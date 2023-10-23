import socket
import logging
import struct
import dotenv
import os
from pydantic import BaseModel
from .messages import Msg
from .messages import MessageABC

logger = logging.getLogger(__name__)


class CyclerInterface:
    """
    Class for interfacing with Arbin battery cycler at a cycler level.
    """

    def __init__(self, config: dict, env_path: str = os.path.join(os.getcwd(), '.env')):
        """
        Creates a class instance for interfacing with Arbin battery cycler at a cycler level.

        Parameters
        ----------
        config : dict
            A configuration dictionary. Must contain the following keys:
                ip_address : str 
                    The IP address of the Arbin host computer.
                port : int 
                    The TCP port to communicate through.
                timeout_s : *optional* : float 
                    How long to wait before timing out on TCP communication. Defaults to 3 seconds. 
                msg_buffer_size : *optional* : int 
                    How big of a message buffer to use for sending/receiving messages. 
                    A minimum of 1024 bytes is recommended. Defaults to 4096 bytes. 
        env_path : *optional* : str
            The path to the `.env` file containing the Arbin CTI username,`ARBIN_CTI_USERNAME`, and password, `ARBIN_CTI_PASSWORD`.
            Defaults to looking in the working directory.
        """
        self.__config = CyclerInterfaceConfig(**config)
        assert(self.__create_connection( 
            ip=self.__config.ip_address, port=self.__config.port, timeout_s=self.__config.timeout_s))
        assert(self.__login(env_path))
        self.__num_channels = self.get_login_feedback()['num_channels']

    def get_num_channels(self):
        '''
        Returns the number of channels on the cycler
        '''
        return self.__num_channels

    def get_login_feedback(self):
        """
        Returns the login feedback message.
        """
        return self.__login_feedback

    def read_channel_status(self, channel: int) -> dict:
        """
        Reads the channel status for the passed channel.

        Parameters
        ----------
        channel : int
            The channel to read the status for.

        Returns
        -------
        status : dict
            A dictionary detailing the status of the channel. Returns None if there is an issue.
        """
        channel_info_msg_rx_dict = {}

        if (channel > self.__num_channels) or (channel < 0):
            logger.error(f'Invalid channel value {channel}!')
            return channel_info_msg_rx_dict

        try:
            # Subtract one from the passed channel value to account for zero indexing
            channel_info_msg_tx = Msg.ChannelInfo.Client.pack(
                {'channel': (channel-1)})
            response_msg_bin = self._send_receive_msg(
                channel_info_msg_tx)

            if response_msg_bin:
                channel_info_msg_rx_dict = Msg.ChannelInfo.Server.unpack(
                    response_msg_bin)
        except Exception as e:
            logger.error(
                f'Error reading channel status for channel {channel}', exc_info=True)
            logger.error(e)

        return channel_info_msg_rx_dict

    def _send_receive_msg(self, tx_msg):
        """
        Sends the passed message and receives the response.

        Parameters
        ----------
        tx_msg : bytearray
            Message to send.

        Returns
        -------
        rx_msg : bytearray
            Response message..
        """

        rx_msg = b''
        send_msg_success = False

        msg_length_format = MessageABC.base_template['msg_length']['format']
        msg_length_start_byte_idx = MessageABC.base_template['msg_length']['start_byte']
        msg_length_end_byte_idx = msg_length_start_byte_idx + \
            struct.calcsize(msg_length_format)

        if self.__sock:
            try:
                self.__sock.sendall(tx_msg)
                send_msg_success = True
            except socket.timeout:
                logger.error(
                    "Timeout on sending message from Arbin!", exc_info=True)
            except socket.error as e:
                logger.error(
                    "Failed to send message to Arbin!", exc_info=True)
                logger.error(e)

            if send_msg_success:
                try:
                    # Receive first part of message and determine length of entire message.
                    rx_msg += self.__sock.recv(self.__config.msg_buffer_size)
                    expected_rx_msg_len = struct.unpack(
                        msg_length_format,
                        rx_msg[msg_length_start_byte_idx:msg_length_end_byte_idx])[0]

                    # Keep reading message in pieces until rx_msg is as long as expected_rx_msg_len.
                    while len(rx_msg) < (expected_rx_msg_len):
                        rx_msg += self.__sock.recv(self.__config.msg_buffer_size)
                except socket.timeout:
                    logger.error(
                        "Timeout on receiving message from Arbin!", exc_info=True)
                except socket.error as e:
                    logger.error(
                        "Error receiving message from Arbin!", exc_info=True)
                    logger.error(e)
                except struct.error as e:
                    logger.error(
                        "Error unpacking message from Arbin!", exc_info=True)
                    logger.error(e)
        else:
            logger.error(
                "Cannot send message! Socket does not exist!")

        return rx_msg

    def __create_connection(self, ip: str, port: int, timeout_s: float) -> bool:
        """
        Creates a TCP/IP connection with Arbin server.

        Parameters
        ----------
        ip : str
            The IP address of the Arbin cycler computer.
        port : int
            the port to connect to.

        Returns
       ----------
        success : bool
            True/False based on whether or not the Arbin server connection was created.
        """
        success = False

        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.settimeout(timeout_s)
            self.__sock.connect((ip, port))
            logger.info("Connected to Arbin server!")
            success = True
        except Exception as e:
            logger.error(
                "Failed to create TCP/IP connection with Arbin server!", exc_info=True)
            logger.error(e)

        return success

    def __login(self, env_path: str) -> bool:
        """
        Logs into the Arbin server with the username/password given in the env file defined in the path. 
        Must be done before issuing other commands.

        Returns
        -------
        success : bool
            True/False based on whether the login was successful
        """
        success = False

        logger.info(f'Loading environment variables from {env_path}')
        dotenv.load_dotenv(env_path, override=True)

        # Validate username and password are in the .env file.
        if not os.getenv('ARBIN_CTI_USERNAME'):
            raise ValueError('ARBIN_CTI_USERNAME not set in environment variables.')
        if not os.getenv('ARBIN_CTI_PASSWORD'):
            raise ValueError('ARBIN_CTI_PASSWORD not set in environment variables.')

        login_msg_tx = Msg.Login.Client.pack(
            msg_values={'username': os.getenv('ARBIN_CTI_USERNAME'), 'password': os.getenv('ARBIN_CTI_PASSWORD')})

        response_msg_bin = self._send_receive_msg(login_msg_tx)

        if response_msg_bin:
            login_msg_rx_dict = Msg.Login.Server.unpack(response_msg_bin)
            if login_msg_rx_dict['result'] == 'success':
                success = True
                logger.info(
                    "Successfully logged in to cycler " + str(login_msg_rx_dict['cycler_sn']))
                logger.info(login_msg_rx_dict)
            elif login_msg_rx_dict['result'] == "already logged in":
                success = True
                logger.warning(
                    "Already logged in to cycler " + str(login_msg_rx_dict['cycler_sn']))
            elif login_msg_rx_dict['result'] == 'fail':
                logger.error(
                    "Login failed with provided credentials!")
            else:
                logger.error(
                    f'Unknown login result {login_msg_rx_dict["result"]}')

            self.__login_feedback = login_msg_rx_dict

        return success
    
class CyclerInterfaceConfig(BaseModel):
    '''
    Holds channel config information for the CyclerInterface class.

    Parameters
    ----------
        ip_address : str 
            The IP address of the Arbin host computer.
        port : int 
            The TCP port to communicate through.
        timeout_s : float 
            How long to wait before timing out on TCP communication. Defaults to 3 seconds. 
        msg_buffer_size : int 
             How big of a message buffer to use for sending/receiving messages. 
            A minimum of 1024 bytes is recommended. Defaults to 4096 bytes. 
    '''
    ip_address: str
    port: int
    timeout_s: float = 3.0
    msg_buffer_size: int = 4096