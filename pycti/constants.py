import struct

class Constants:
    
    class TX_MSG:
        TIMEOUT_S = 3

        # Fixed value,	unsigned long long (8 bytes)
        HEADER_FORMAT = '<Q'
        HEADER = 0x11DDDDDDDDDDDDDD
        HEADER_BYTEARRAY = struct.pack(HEADER_FORMAT, HEADER)

        BUFFER_SIZE_BYTES = 2**10
        class LOGIN:

            # Message length unsigned long (4 bytes)
            MSG_LENGTH_FORMAT = '<L'
            # Command Code (4 bytes) + Extended command code (4 bytes) + Username (32 bytes) + Password (32 bytes) + Checksum (2 bytes)
            MSG_LENGTH = 74
            MSG_LENGTH_BYTEARRAY = struct.pack(MSG_LENGTH_FORMAT, MSG_LENGTH)

            # Command codes, unsigned long (4 bytes)
            COMMAND_CODE_FORMAT = '<L'
            COMMAND_CODE = 0xEEAB0001
            COMMAND_CODE_BYTEARRAY = struct.pack(COMMAND_CODE_FORMAT, COMMAND_CODE)

            # Fixed value 0x00000000, unsigned long (4 bytes)
            EXTENDED_COMMAND_FORMAT = '<L'
            EXTENDED_COMMAND_CODE = 0x00000000
            EXTENDED_COMMAND_CODE_BYTEARRAY = struct.pack(EXTENDED_COMMAND_FORMAT, EXTENDED_COMMAND_CODE)

            # Strings are 32 byte character arrays
            STRING_FORMAT = '32s'
            STRING_ENCODING = 'ascii'



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



