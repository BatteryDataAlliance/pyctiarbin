class Constants:
    
    class TX_MSG:
        TIMEOUT_S = 3

        BUFFER_SIZE_BYTES = 2**10

        # Fixed value,	unsigned long long (8 bytes)
        HEADER_FORMAT = '<Q'
        HEADER = 0x11DDDDDDDDDDDDDD

        MSG_LENGTH_FORMAT = '<L'
        MSG_LENGTH = {
            # Command Code (4 bytes) + Extended command code (4 bytes) + Username (32 bytes) + Password (32 bytes) + Checksum (2 bytes)
            "LOGIN" : 74
        }

        # Command codes, unsigned long (4 bytes)
        COMMAND_CODE_FORMAT = '<L'
        COMMAND_CODES = {
            "LOGIN": 0xEEAB0001,
            "GET_CHANNELS_INFO": 0xEEAB0003,
            "SET_METAVARIABLE_VALUE": 0xBB150001,
            "SCHEDULE_START": 0xBB320004,
            "SCHEDULE_STOP": 0xBB310001,
            "SCHEDULE_JUMP": 0xBB320005
        }

        # Strings are 32 byte character arrays
        STRING_FORMAT = '32s'
        STRING_ENCODING = 'ascii'

        # Fixed value 0x00000000, unsigned long (4 bytes)
        EXTENDED_COMMAND_FORMAT = '<L'
        EXTENDED_COMMAND_CODE = 0x00000000

    class RX_MSG:
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



