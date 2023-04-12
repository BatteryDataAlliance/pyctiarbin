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

    cycler_sn = None

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
        self.channel = config['channel'] - 1
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
                if self.__arbin_login():
                    success = True

        return success

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

        # # Prepare the pieces of the login message
        packed_header = struct.pack(
            Constants.TX_MSG.HEADER_FORMAT, Constants.TX_MSG.HEADER)
        packed_msg_length = struct.pack(
            Constants.TX_MSG.MSG_LENGTH_FORMAT, Constants.TX_MSG.MSG_LENGTH['LOGIN'])
        packed_command_code = struct.pack(
            Constants.TX_MSG.COMMAND_CODE_FORMAT, Constants.TX_MSG.COMMAND_CODES["LOGIN"])
        packed_command_code_extended = struct.pack(
            Constants.TX_MSG.EXTENDED_COMMAND_FORMAT, Constants.TX_MSG.EXTENDED_COMMAND_CODE)
        packed_username = struct.pack(
            Constants.TX_MSG.STRING_FORMAT, username.encode(Constants.TX_MSG.STRING_ENCODING))
        packed_password = struct.pack(
            Constants.TX_MSG.STRING_FORMAT, password.encode(Constants.TX_MSG.STRING_ENCODING))
        # Put the message together
        login_msg_tx = packed_header + packed_msg_length + packed_command_code + \
            packed_command_code_extended + packed_username + packed_password
        # Add the checksum at the end
        login_msg_tx += struct.pack('<H', sum(login_msg_tx))

        # Receive message response and parse it
        login_msg_rx = self.__send_receive_msg(login_msg_tx)
        if login_msg_rx:
            # Get login result
            login_result = struct.unpack(
                Constants.RX_MSG.LOGIN.RESULT_FORMAT,
                login_msg_rx[Constants.RX_MSG.LOGIN.RESULT_START_BYTE:Constants.RX_MSG.LOGIN.RESULT_END_BYTE])[0]
            if login_result == Constants.RX_MSG.LOGIN.SUCESS_RESULT_CODE:
                success = True
                logger.info("Login success!")
            elif login_result == Constants.RX_MSG.LOGIN.ALREADY_LOGGED_IN_CODE:
                success = True
                logger.info("Already logged in!")
            elif login_result == Constants.RX_MSG.LOGIN.FAIL_RESULT_CODE:
                logger.error("Login failed with provided credentials!")
            else:
                logger.error("Unknown login result response code")

            # Get cycler serial number
            cycler_sn_bytearray = struct.unpack(
                Constants.RX_MSG.LOGIN.SERIAL_NUMBER_FORMAT,
                login_msg_rx[Constants.RX_MSG.LOGIN.SERIAL_NUMBER_START_BYTE:Constants.RX_MSG.LOGIN.SERIAL_NUMBER_END_BYTE])[0]
            self.cycler_sn = cycler_sn_bytearray.decode(Constants.RX_MSG.LOGIN.SERIAL_NUMBER_ENCODING)
            print(self.cycler_sn)

        return success

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
            self.__sock.settimeout(Constants.TX_MSG.TIMEOUT_S)
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
        Sends the passed message and receives the response.

        Parameters
        ----------
        tx_msg : bytearray
            Message to send to the server.

        Returns
        -------
        rx_msg : bytearray
            Response message from the server.
        """

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
                rx_msg += self.__sock.recv(Constants.TX_MSG.BUFFER_SIZE_BYTES)
                rx_msg_len = struct.unpack('<L', rx_msg[8:12])[0]
                while len(rx_msg) < rx_msg_len:
                    rx_msg += self.__sock.recv(
                        Constants.TX_MSG.BUFFER_SIZE_BYTES)
            except:
                logger.error("Error receiving TX_MSG", exc_info=True)

        return rx_msg
