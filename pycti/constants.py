class Constants:
    
    class MSG:
        TIMEOUT_S = 3

        BUFFER_SIZE_BYTES = 2**10

        HEADER = 0x11DDDDDDDDDDDDDD

        COMMAND_CODES = {
            "USER_LOGIN_CMD": 0xEEAB0001,
            "GET_CHANNELS_INFO": 0xEEAB0003,
            "SET_METAVARIABLE_VALUE": 0xBB150001,
            "SCHEDULE_START": 0xBB320004,
            "SCHEDULE_STOP": 0xBB310001,
            "SCHEDULE_JUMP": 0xBB320005
        }