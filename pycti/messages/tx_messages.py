import struct


class TX_MSG:

    # Fixed value, unsigned long long (8 bytes)
    HEADER_FORMAT = '<Q'
    HEADER = 0x11DDDDDDDDDDDDDD
    HEADER_BYTEARRAY = struct.pack(HEADER_FORMAT, HEADER)

    class LOGIN:

        # Message length unsigned long (4 bytes)
        MSG_LENGTH_FORMAT = '<L'
        # Command Code (4 bytes) + Extended command code (4 bytes) + Username (32 bytes) + Password (32 bytes) + Checksum (2 bytes)
        MSG_LENGTH = 74
        MSG_LENGTH_BYTEARRAY = struct.pack(
            MSG_LENGTH_FORMAT, MSG_LENGTH)

        # Command codes, unsigned long (4 bytes)
        COMMAND_CODE_FORMAT = '<L'
        COMMAND_CODE = 0xEEAB0001
        COMMAND_CODE_BYTEARRAY = struct.pack(
            COMMAND_CODE_FORMAT, COMMAND_CODE)

        # Fixed value 0x00000000, unsigned long (4 bytes)
        EXTENDED_COMMAND_FORMAT = '<L'
        EXTENDED_COMMAND_CODE = 0x00000000
        EXTENDED_COMMAND_CODE_BYTEARRAY = struct.pack(
            EXTENDED_COMMAND_FORMAT, EXTENDED_COMMAND_CODE)

        # Strings are 32 byte character arrays
        STRING_FORMAT = '32s'
        STRING_ENCODING = 'ascii'

        def build_msg(username: str, password: str) -> bytearray:
            """
            Returns a complete byte array message to send for login.

            Parameters
            ----------
            username : str
                Arbin username
            password : str
                Arbin password

            Returns
            -------
            msg : bytearray
                Complete message
            """
            msg = bytearray([])
            msg += TX_MSG.HEADER_BYTEARRAY
            msg += TX_MSG.LOGIN.MSG_LENGTH_BYTEARRAY
            msg += TX_MSG.LOGIN.COMMAND_CODE_BYTEARRAY
            msg += TX_MSG.LOGIN.EXTENDED_COMMAND_CODE_BYTEARRAY
            msg += struct.pack(
                TX_MSG.LOGIN.STRING_FORMAT, username.encode(TX_MSG.LOGIN.STRING_ENCODING))
            msg += struct.pack(
                TX_MSG.LOGIN.STRING_FORMAT, password.encode(TX_MSG.LOGIN.STRING_ENCODING))
            msg += struct.pack('<H', sum(msg))  # Checksum
            return msg

    class CHAN_INFO:

        # Message length unsigned long (4 bytes)
        MSG_LENGTH_FORMAT = '<L'
        # Command Code (4 bytes) + Extended command code (4 bytes) + Channel (2 bytes) + Channel Format (2 bytes) + Aux Options (4 bytes) + Reserved Bytes (32) +  Checksum (2 bytes)
        4+4+2+2+4+32+2
        MSG_LENGTH = 50
        MSG_LENGTH_BYTEARRAY = struct.pack(
            MSG_LENGTH_FORMAT, MSG_LENGTH)

        # Command codes, unsigned long (4 bytes)
        COMMAND_CODE_FORMAT = '<L'
        COMMAND_CODE = 0xEEAB0003
        COMMAND_CODE_BYTEARRAY = struct.pack(
            COMMAND_CODE_FORMAT, COMMAND_CODE)

        # Fixed value 0x00000000, unsigned long (4 bytes)
        EXTENDED_COMMAND_FORMAT = '<L'
        EXTENDED_COMMAND_CODE = 0x00000000
        EXTENDED_COMMAND_CODE_BYTEARRAY = struct.pack(
            EXTENDED_COMMAND_FORMAT, EXTENDED_COMMAND_CODE)

        # Channel is set in program. Format is short (2 bytes)
        CHANNEL_FORMAT = 'h'

        # Channel format is short (2 bytes)
        CHANNEL_SELECTION_FORMAT = 'h'
        # 1: All Channels, 2: Running Channel, 3: Unsafe Channel. I think this is only used is 0 is set for channel
        CHANNEL_SELECTION = 1
        CHANNEL_SELECTION_BYTEARRAY = struct.pack(
            CHANNEL_SELECTION_FORMAT, CHANNEL_SELECTION)

        # Aux options, unsigned long (4 bytes)
        AUX_OPTIONS_FORMAT = '<L'
        AUX_REQUIRES_NONE = 0x00000000
        AUX_REAQUIRES_BMS = 0x10000000
        AUX_REAQUIRES_SMB = 0x20000000
        AUX_REAQUIRES_AUX = 0x40000000

        # These are reserved and not used.
        RESERVED_BYTES = bytearray([0x00 for i in range(32)])

        def build_msg(channel: int, req_bms=False, req_smb=False, req_aux=False):
            """
            Returns a complete byte array message to send for channel info.

            Parameters
            ----------
            channel : int
                The Arbin channel to select infor for. Note Arbin zero indexes.
            req_bms : bool
                Whether or not BMS data is required. Defaults to False.
            req_smb : bool
                Whether or not SMB data is required. Defaults to False.
            req_aux : bool
                Whether or not AUX data is required. Defaults to False.

            Returns
            -------
            rx_msg : bytearray
                Response message from the server.
            """
            msg = bytearray([])
            msg += TX_MSG.HEADER_BYTEARRAY
            msg += TX_MSG.CHAN_INFO.MSG_LENGTH_BYTEARRAY
            msg += TX_MSG.CHAN_INFO.COMMAND_CODE_BYTEARRAY
            msg += TX_MSG.CHAN_INFO.EXTENDED_COMMAND_CODE_BYTEARRAY
            msg += struct.pack(TX_MSG.CHAN_INFO.CHANNEL_FORMAT, channel)
            msg += TX_MSG.CHAN_INFO.CHANNEL_SELECTION_BYTEARRAY
            # TODO : Figure out Aux options
            msg += struct.pack('<L', 0)
            msg += TX_MSG.CHAN_INFO.RESERVED_BYTES
            msg += struct.pack('<H', sum(msg))  # Checksum

            return msg