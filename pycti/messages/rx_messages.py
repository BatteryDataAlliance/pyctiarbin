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
            
            login_result = struct.unpack(
                RX_MSG.LOGIN.RESULT_FORMAT,
                msg[RX_MSG.LOGIN.RESULT_START_BYTE:RX_MSG.LOGIN.RESULT_END_BYTE])[0]
            msg_dict['login_result'] = login_result

            cycler_sn_bytearray = struct.unpack(
                RX_MSG.LOGIN.SERIAL_NUMBER_FORMAT,
                msg[RX_MSG.LOGIN.SERIAL_NUMBER_START_BYTE:RX_MSG.LOGIN.SERIAL_NUMBER_END_BYTE])[0]
            msg_dict['cycler_sn'] = cycler_sn_bytearray.decode(RX_MSG.LOGIN.SERIAL_NUMBER_ENCODING)

            # TODO : Parse more of the message

            return msg_dict
        

    class CHAN_INFO:

        # Result is reported as unsigned int (4 bytes)
        NUM_OF_CHANNELS_FORMAT = '<L'
        NUM_OF_CHANNEL_START_BYTE = 20
        NUM_OF_CHANNEL_END_BYTE = NUM_OF_CHANNEL_START_BYTE + 4

        # Result is reported as unsigned int (4 bytes) # NOT WORKING!!!!
        CHANNEL_INDEX_FORMAT = '<I'
        CHANNEL_INDEX_FORMAT_START_BYTE = 24
        CHANNEL_INDEX_FORMAT_END_BYTE = CHANNEL_INDEX_FORMAT_START_BYTE + 4

        # Status reported as short
        STATUS_FORMAT = '<h'
        STATUS_START_BYTE = 28
        STATUS_END_BYTE = STATUS_START_BYTE + 2

        # Schedule is a array of 200 `wchar_t` types, which are 2 bytes each
        SCHEDULE_FORMAT = '400s'
        SCHEDULE_FORMAT_START_BYTE = 31
        SCHEDULE_FORMAT_END_BYTE = SCHEDULE_FORMAT_START_BYTE + 400
        SCHEDULE_FORMAT_ENCODING = 'utf-16'

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
            
            num_channels = struct.unpack(
                RX_MSG.CHAN_INFO.NUM_OF_CHANNELS_FORMAT,
                msg[RX_MSG.CHAN_INFO.NUM_OF_CHANNEL_START_BYTE:RX_MSG.CHAN_INFO.NUM_OF_CHANNEL_END_BYTE])[0]
            msg_dict['num_channels'] = num_channels

            channel_index = struct.unpack(
                RX_MSG.CHAN_INFO.CHANNEL_INDEX_FORMAT,
                msg[RX_MSG.CHAN_INFO.CHANNEL_INDEX_FORMAT_START_BYTE:RX_MSG.CHAN_INFO.CHANNEL_INDEX_FORMAT_END_BYTE])[0]
            msg_dict['channel_index'] = channel_index

            status = struct.unpack(
                RX_MSG.CHAN_INFO.STATUS_FORMAT,
                msg[RX_MSG.CHAN_INFO.STATUS_START_BYTE:RX_MSG.CHAN_INFO.STATUS_END_BYTE])[0]
            msg_dict['status'] = RX_MSG.CHAN_INFO.STATUS_CODES[status]

            schedule_name = struct.unpack(
                RX_MSG.CHAN_INFO.SCHEDULE_FORMAT,
                msg[RX_MSG.CHAN_INFO.SCHEDULE_FORMAT_START_BYTE:RX_MSG.CHAN_INFO.SCHEDULE_FORMAT_END_BYTE])[0]
            msg_dict['schedule_name'] = schedule_name.decode(RX_MSG.CHAN_INFO.SCHEDULE_FORMAT_ENCODING).rstrip('\x00')

            return msg_dict



        
