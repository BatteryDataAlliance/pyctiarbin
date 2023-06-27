import socket
import logging
import struct
from .messages import Msg
from .messages import MessageABC

logger = logging.getLogger(__name__)


class CyclerInterface:
    """
    Class for interfacing with Arbin battery cycler at a cycler-level.
    """

    def __init__(self, config: dict):
        """
        A class for interfacing with the Arbin cycler.

        Parameters
        ----------
        config : dict
            A configuration dictionary. Must contain the following keys:
            - `ip_address` - The IP address of the Maccor server. Use 127.0.0.1 if running on the same machine as the server.
            - `port` - The port to communicate through with JSON messages. Default set to 57570.
            - `msg_buffer_size_bytes` - How big of a message buffer to use for sending/receiving messages. A minimum of 1024 bytes is recommended.
        """

        # Copy the verify the config
        self.__config = config
        assert(self.__verify_config())


        self.__tcp_timeout_s = 2

        
        assert(self.__create_connection())
        assert(self.__login())

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

        channel_info_msg_tx = Msg.ChannelInfo.Client.pack(
            {'channel': channel})
        response_msg_bin = self._send_receive_msg(
            channel_info_msg_tx)

        if response_msg_bin:
            channel_info_msg_rx_dict = Msg.ChannelInfo.Server.unpack(
                response_msg_bin)

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
            except socket.error:
                logger.error(
                    "Failed to send message to Arbin!", exc_info=True)

            if send_msg_success:
                try:
                    # Receive first part of message and determine length of entire message.
                    rx_msg += self.__sock.recv(
                        self.__config['msg_buffer_size'])
                    expected_rx_msg_len = struct.unpack(
                        msg_length_format,
                        rx_msg[msg_length_start_byte_idx:msg_length_end_byte_idx])[0]

                    # Keep reading message in pieces until rx_msg is as long as expected_rx_msg_len.
                    while len(rx_msg) < (expected_rx_msg_len):
                        rx_msg += self.__sock.recv(
                            self.__config['msg_buffer_size'])
                except socket.timeout:
                    logger.error(
                        "Timeout on receiving message from Arbin!", exc_info=True)
                except socket.error:
                    logger.error(
                        "Error receiving message from Arbin!", exc_info=True)
        else:
            logger.error(
                "Cannot send message! Socket does not exist!")

        return rx_msg

    def __verify_config(self) -> bool:
        """
        Verifies that the config passed on construction is valid.

        Returns
        --------------------------
        success : bool
            True/False based on whether the config passed at construction is valid.
        """
        required_config_keys = ['username',
                                'password',
                                'test_name',
                                'schedule',
                                'channel',
                                'ip_address',
                                'port',
                                'timeout_s',
                                'msg_buffer_size']

        for key in required_config_keys:
            if key not in self.__config:
                logger.error("Missing key from config! Missing : " + key)
                return False
        logger.info("Config check passed")
        return True

    def __create_connection(self) -> bool:
        """
        Creates a TCP/IP connection with Arbin server.

        Returns
       ----------
        success : bool
            True/False based on whether or not the Arbin server connection was created.
        """
        success = False

        try:
            self.__sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self.__sock.settimeout(self.__tcp_timeout_s)
            self.__sock.connect(
                (self.__config['ip_address'], self.__config['port'])
            )
            logger.info("Connected to Arbin server!")
            success = True
        except:
            logger.error(
                "Failed to create TCP/IP connection with Arbin server!", exc_info=True)

        return success

    def __login(self) -> bool:
        """
        Logs into the Arbin server with the username/password defined in the config. 
        Must be done before issuing other commands.

        Returns
        -------
        success : bool
            True/False based on whether the login was successful
        """
        success = False

        login_msg_tx = Msg.Login.Client.pack(
            msg_values={'username': self.__config['username'], 'password': self.__config['password']})

        response_msg_bin = self._send_receive_msg(login_msg_tx)

        if response_msg_bin:
            login_msg_rx_dict = Msg.Login.Server.unpack(response_msg_bin)

            if login_msg_rx_dict['result'] == 'success':
                success = True
                logger.info(
                    "Successfully logged in to cycler " + str(login_msg_rx_dict['cycler_sn']))
            # Typo is on purpose
            elif login_msg_rx_dict['result'] == "aleady logged in":
                success = True
                logger.info(
                    "Already logged in to cycler " + str(login_msg_rx_dict['cycler_sn']))
            elif login_msg_rx_dict['result'] == 'fail':
                logger.error(
                    "Login failed with provided credentials!")
            else:
                logger.error(
                    f'Unknown login result {login_msg_rx_dict["result"]}')

            self.__login_feedback = login_msg_rx_dict

        return success