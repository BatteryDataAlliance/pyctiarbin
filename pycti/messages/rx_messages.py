import struct


class RX_MSG:

    BUFFER_SIZE = 2**12

    MSG_LENGTH_FORMAT = '<L'
    MSG_LENGTH_START_BYTE = 8
    MSG_LENGTH_END_BYTE = 12

    # Fixed value, unsigned long long (8 bytes)
    Prefix_FORMAT = '<Q'
    Prefix = 0x11DDDDDDDDDDDDDD
    Prefix_BYTEARRAY = struct.pack(Prefix_FORMAT, Prefix)

    class LOGIN:

        SUCESS_RESULT_CODE = 1
        FAIL_RESULT_CODE = 2
        ALREADY_LOGGED_IN_CODE = 3

        # Serial number is string of length 16
        SERIAL_NUMBER_FORMAT = '16s'
        SERIAL_NUMBER_START_BYTE = 28
        SERIAL_NUMBER_END_BYTE = SERIAL_NUMBER_START_BYTE + 16
        SERIAL_NUMBER_ENCODING = 'ascii'

        def parse_msg(msg: bytearray) -> dict:
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

            login_result = struct.unpack(
                RX_MSG.LOGIN.RESULT_FORMAT,
                msg[RX_MSG.LOGIN.RESULT_START_BYTE:RX_MSG.LOGIN.RESULT_END_BYTE])[0]
            msg_dict['login_result'] = login_result

            cycler_sn_bytearray = struct.unpack(
                RX_MSG.LOGIN.SERIAL_NUMBER_FORMAT,
                msg[RX_MSG.LOGIN.SERIAL_NUMBER_START_BYTE:RX_MSG.LOGIN.SERIAL_NUMBER_END_BYTE])[0]
            msg_dict['cycler_sn'] = cycler_sn_bytearray.decode(
                RX_MSG.LOGIN.SERIAL_NUMBER_ENCODING)

            # TODO : Parse more of the message

            return msg_dict

    class CHAN_INFO:

        # Codes for reading back the status value
        STATUS_CODES = [
            'Idle',
            'Transition',
            'Charge',
            'Discharge',
            'Rest',
            'Wait',
            'External Charge',
            'Calibration',
            'Unsafe',
            'Pulse',
            'Internal Resistance',
            'AC Impedance',
            'ACI Cell',
            'Test Settings',
            'Error',
            'Finished',
            'Volt Meter',
            'Waiting for ACS',
            'Pause',
            'Empty',
            'Idle from MCU',
            'Start',
            'Runnng',
            'Step Transfer',
            'Resume',
            'Go Pause',
            'Go Stop',
            'Go Next Step',
            'Online Update',
            'DAQ Memoery Unsafe',
            'ACR'
        ]

        msg_encoding = {
            'num_channels': {
                'format': '<L',
                'start_byte': 20,
                'size': 4,
            },
            'channel_index': {
                'format': '<I',
                'start_byte': 24,
                'size': 4,
            },
            'status': {
                'format': '<h',
                'start_byte': 28,
                'size': 2,
            },
            'test_name': {
                'format': '144s',
                'start_byte': 431,
                'size': 144,
                'text_encoding': 'utf-16'
            },
            'exit_condition': {
                'format': '200s',
                'start_byte': 575,
                'size': 200,
                'text_encoding': 'utf-16'
            },
            'step_and_cycle': {
                'format': '128s',
                'start_byte': 775,
                'size': 128,
                'text_encoding': 'utf-16'
            },
        }

        # Test Time reported as double (8 bytes)
        '''
        TEST_TIME_FORMAT = '<d'
        TEST_TIME_START_BYTE = 1849
        TEST_TIME_END_BYTE = TEST_TIME_START_BYTE + 8
            #struct.calcsize(TEST_TIME_FORMAT)
        '''

        def parse_msg(msg: bytearray) -> dict:
            """
            Prases the passed message.

            Returns
            -------
            msg_dict : dict
                The message response as a dictionary
            """
            msg_dict = {}

            for data_name, encoding in RX_MSG.CHAN_INFO.msg_encoding.items():
                msg_dict[data_name] = struct.unpack(
                    encoding['format'],
                    msg[encoding['start_byte']:encoding['start_byte']+encoding['size']])[0]
                # Strip decode and strip trailing 0s from strings.
                if encoding['format'].endswith('s'):
                    msg_dict[data_name] = msg_dict[data_name].decode(
                        encoding['text_encoding']).rstrip('\x00')

            return msg_dict
