class RX_MSG:

    BUFFER_SIZE = 2**12

    MSG_LENGTH_FORMAT = '<L'
    MSG_LENGTH_START_BYTE = 8
    MSG_LENGTH_END_BYTE = 12

    class LOGIN:

        # Result is reported as unsigned int (4 bytes)
        RESULT_FORMAT = 'I'
        RESULT_START_BYTE = 20
        RESULT_END_BYTE = RESULT_START_BYTE + 4

        SUCESS_RESULT_CODE = 1
        FAIL_RESULT_CODE = 2
        ALREADY_LOGGED_IN_CODE = 3

        # Serial number is string of length 16
        SERIAL_NUMBER_FORMAT = '16s'
        SERIAL_NUMBER_START_BYTE = 28
        SERIAL_NUMBER_END_BYTE = SERIAL_NUMBER_START_BYTE + 16
        SERIAL_NUMBER_ENCODING = 'ascii'

        def parse_msg(msg : bytearray) -> dict:
            """
            Prases the passed message

            Parameters
            ----------
            username : str
                Arbin username
            password : str
                Arbin password

            Returns
            -------
            msg_dict : dict
                The message response as a dictionary
            """
            msg_dict = {}

        # Receive message response and parse it
        login_msg_rx = self.__send_receive_msg(login_msg_tx)
        if login_msg_rx:
            # Get login result
            login_result = struct.unpack(
                RX_MSG.LOGIN.RESULT_FORMAT,
                login_msg_rx[RX_MSG.LOGIN.RESULT_START_BYTE:RX_MSG.LOGIN.RESULT_END_BYTE])[0]
            if login_result == RX_MSG.LOGIN.SUCESS_RESULT_CODE:
                success = True
                logger.info("Login success!")
            elif login_result == RX_MSG.LOGIN.ALREADY_LOGGED_IN_CODE:
                success = True
                logger.info("Already logged in!")
            elif login_result == RX_MSG.LOGIN.FAIL_RESULT_CODE:
                logger.error("Login failed with provided credentials!")
            else:
                logger.error("Unknown login result response code!")

            # Get cycler serial number
            cycler_sn_bytearray = struct.unpack(
                RX_MSG.LOGIN.SERIAL_NUMBER_FORMAT,
                login_msg_rx[RX_MSG.LOGIN.SERIAL_NUMBER_START_BYTE:RX_MSG.LOGIN.SERIAL_NUMBER_END_BYTE])[0]
            self.cycler_sn = cycler_sn_bytearray.decode(
                RX_MSG.LOGIN.SERIAL_NUMBER_ENCODING)
            logger.info("Cycler SN: " + str(self.cycler_sn))

        return success


        
