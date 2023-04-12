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
        
