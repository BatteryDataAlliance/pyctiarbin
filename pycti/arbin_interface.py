import socket
import logging
import struct
import copy

from .constants import Constants

logger = logging.getLogger(__name__)


class ArbinInterface:
    """
    Class for controlling Maccor Cycler using MacNet.
    """

    def __init__(self, config: dict):
        """
        Creates a class instance. The `start()` method still needs to be run to create the connection
        and to check the validity of the config.

        Parameters
        ----------
        config : dict
            A configuration dictionary.
        """

        # Channels are zero indexed within CTI so we must subtract one here.
        self.channel = config['channel'] -1
        self.config = config
        self.__sock = None

    def start(self) -> bool:
        """
        Verifies the config, creates a connection to the Arbin, and logs in.

        Returns
        -------
        success : bool
            True or False based on whether or not the connection was created.
        """
        success = False

        if self.__verify_config():
            if self.__create_connection():
                pass
                #if self.__arbin_login():
                #    success = True
        return self.__arbin_login()
        
    def read_status(self) -> dict:
        """
        Method to read the status of the channel defined in the config.

        Returns
        -------
        status : dict
            A dictionary detailing the status of the channel. Returns None if there is an issue.
        """
        return {}
        
    def __verify_config(self) -> bool:
        """
        Verifies that the config passed on construction is valid.

        Returns
        --------------------------
        success : bool
            True or False based on whether the config passed at construction is valid.
        """
        required_config_keys = ['username',
                                'password',
                                'test_name',
                                'schedule',
                                'channel',
                                'arbin_ip',
                                'arbin_port']

        for key in required_config_keys:
            if key not in self.config:
                logger.error("Missing key from config! Missing : " + key)
                return False
        logger.info("Verified config")
        return True
        

    def __arbin_login(self) -> bool:
        """
        Logs into the Arbin server with the username/password defined in the config. 
        Must be done before issuing other commands.

        Returns
        -------
        success : bool
            True or False based on whether the login was successful
        """
        success = False

        username = '123'
        password = '123'
        login_msg = bytearray([])
        login_msg += struct.pack('<Q', Constants.MSG.HEADER)
        login_msg += struct.pack('<L', 4+4+32+32+2)
        login_msg += struct.pack('<LL', Constants.MSG.COMMAND_CODES["USER_LOGIN_CMD"], 0x00000000)
        login_msg += struct.pack('<{}s'.format(len(username)), username.encode('ascii'))
        login_msg += bytearray([0x00 for i in range(32-len(username))])
        login_msg += struct.pack('<{}s'.format(len(password)), password.encode('ascii'))
        login_msg += bytearray([0x00 for i in range(32-len(password))])
        login_msg += struct.pack('<H', sum(login_msg))

        response = self.__send_receive_msg(login_msg)
        success = True

        return response


    def __create_connection(self) -> bool:
        """
        Creates a TCP/IP connection with Arbin server.

        Returns
       ----------
        success : bool
            True or False based on whether or not the connection was created.
        """
        success = False

        try:
            self.__sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self.__sock.settimeout(Constants.MSG.TIMEOUT_S)
            self.__sock.connect(
                (self.config['arbin_ip'], self.config['arbin_port'])
            )
            logger.info("Connected to Arbin server!")
            success = True
        except:
            logger.error(
                "Failed to create TCP/IP connection with Arbin server!", exc_info=True)

        return success

    def __send_receive_msg(self, tx_msg):
        """
        Sends the passed message to the MITS server and receives the response.

        Parameters
        ----------
        tx_msg_bytearray: bytearray
            Msg to be sent to the server.
        
        Returns
        -------
        bytearray:
            Response from the server.
        """
        '''
        
        self.__sock.send(tx_msg_bytearray)
        data = b''
        incoming = self.__sock.recv(Constants.MSG.BUFFER_SIZE_BYTES)
        data_len = struct.unpack('<L', incoming[8:12])[0]
        data += incoming
        while len(data) < data_len:
            try:
                print("here")
                incoming = self.__sock.recv(Constants.MSG.BUFFER_SIZE_BYTES)
                print("Now here")
                data += incoming
            except:
                logger.error("Error receiving msg")
                break
        # return self.sock.recv(MSG_BUFFER_SIZE)
        return data
        '''

        rx_msg = b''
        send_msg_success = False

        try:
            self.__sock.send(tx_msg)
            send_msg_success = True 
        except:
            logger.error(
                "Failed to send message to Arbin server!", exc_info=True)

        if send_msg_success:
            try:
                rx_msg += self.__sock.recv(Constants.MSG.BUFFER_SIZE_BYTES)
                rx_msg_len = struct.unpack('<L', rx_msg[8:12])[0]
                while len(rx_msg) < rx_msg_len:
                        rx_msg += self.__sock.recv(Constants.MSG.BUFFER_SIZE_BYTES)
            except:
                logger.error("Error receiving msg", exc_info=True)
                
        return rx_msg
