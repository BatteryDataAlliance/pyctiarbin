import struct
import logging
from copy import deepcopy
from abc import ABC

logger = logging.getLogger(__name__)

# Defines the command codes used for messages
CMD_CODES = {
    'Login': 0xEEAB0001
}


class MessageABC(ABC):

    # The length of the message. Should be overwritten in child class
    msg_length = 0

    # The message command code. Should be overwritten in child class
    command_code = 0x00

    # Templet that is specific to each message type. Should be overwritten in child class
    msg_specific_templet = {}

    # Base message templet that is common for all messasges
    base_templet = {
        'header': {
            'format': '<Q',
            'start_byte': 0,
            'value': 0x11DDDDDDDDDDDDDD
        },
        'msg_length': {
            'format': '<L',
            'start_byte': 8,
            'value': 0
        },
        'command_code': {
            'format': '<L',
            'start_byte': 12,
            'value': 0x00000000
        },
        'extended_command_code': {
            'format': '<L',
            'start_byte': 16,
            'value': 0x00000000
        },
    }

    @classmethod
    def parse_msg(cls, msg: bytearray) -> dict:
        """
        Parses the passed message and decodes it with the msg_encoding dict.
        Each key in the output message will have name of the key from the 
        msg_encoding dictionary.

        Parameters
        ----------
        msg : bytearry
            The message to parse.

        Returns
        -------
        decoded_msg_dict : dict
            The message items decoded into a dictionary.
        """
        decoded_msg_dict = {}

        # Create a templet to parse message with
        templet = {**deepcopy(cls.base_templet),
                   **deepcopy(cls.msg_specific_templet)}

        for item_name, item in templet.items():

            start_idx = item['start_byte']
            end_idx = item['start_byte'] + struct.calcsize(item['format'])

            decoded_msg_dict[item_name] = struct.unpack(
                item['format'], msg[start_idx:end_idx])[0]

            # Decode and strip trailing 0x00s from strings.
            if item['format'].endswith('s'):
                decoded_msg_dict[item_name] = decoded_msg_dict[item_name].decode(
                    item['text_encoding']).rstrip('\x00')

        '''
        TODO : Add check to make sure command code is what we excpet
        if decoded_msg_dict['command_code']['value'] != cls.command_code:
            logger.warning(
                f'Decoded command code {decoded_msg_dict["command_code"]} does not match what was expcected!')
        '''

        return decoded_msg_dict

    @classmethod
    def build_msg(cls, msg_values={}) -> bytearray:
        """
        Packs a message based on the message encoding given in the msg_encoding
        dictionary. Values can be substituted for default values if they are included 
        in the `msg_values` argument

        Parameters
        ----------
        msg_values : dict
            A dictionary detailing which default values in the msg_encoding should be 
            updated.

        Returns
        -------
        msg : bytearray
            Response message from the server.
        """
        # Create a template to build messages from.
        templet = {**deepcopy(cls.base_templet),
                   **deepcopy(cls.msg_specific_templet)}
        
        # Update the templet with message specific length and command code
        templet['msg_length']['value'] = cls.msg_length
        templet['command_code']['value'] = cls.command_code

        print(templet)

        # Create a message bytearray that will be loaded with message contents
        msg = bytearray(templet['msg_length']['value'])

        # Update default msg values with those in the msg_values dict
        for key in msg_values.keys():
            if key in templet.keys():
                templet[key]['value'] = msg_values[key]
            else:
                logger.warning(
                    f'Key name {key} was not found in msg_encoding!')

        for item_name, item in templet.items():
            # Pack the msg item
            logger.debug(f'Packing item {item_name}')
            if item['format'].endswith('s'):
                packed_item = struct.pack(
                    item['format'],
                    item['value'].encode(item['text_encoding']))
            else:
                packed_item = struct.pack(
                    item['format'], item['value'])

            # Put the packed item into the msg bytearray
            start_idx = item['start_byte']
            end_idx = item['start_byte'] + struct.calcsize(item['format'])
            msg[start_idx:end_idx] = packed_item

        # Append a checksum to the end
        msg += struct.pack('<H', sum(msg))

        return msg


class Msg:
    class Login:
        '''
        Message for logging into Arbin cycler.
        '''
        class Client(MessageABC):
            msg_length = 74
            command_code  = CMD_CODES['Login']

            msg_specific_templet = {
                'username': {
                    'format': '32s',
                    'start_byte': 20,
                    'text_encoding': 'utf-8',
                    'value': 123
                },
                'password': {
                    'format': '32s',
                    'start_byte': 52,
                    'text_encoding': 'utf-8',
                    'value': 123
                },
            }

        class Server(MessageABC):
            msg_length = 128
            command_code  = CMD_CODES['Login']

            msg_specific_templet = {
                'result': {
                    'format': 'I',
                    'start_byte': 20,
                    'value': 0
                },
                'cycler_sn': {
                    'format': '16s',
                    'start_byte': 52,
                    'text_encoding': 'ascii',
                    'value': '00000000'
                },
            }

            # Used to decode the login result
            login_result_decoder = [
                "should not see this", "success", "fail", "aleady logged in"]

            @classmethod
            def parse_msg(cls, msg: bytearray) -> dict:
                """
                Same as the parrent class, but converts the result based on the
                login_result_decoder.

                Parameters
                ----------
                msg : bytearry
                    The message to parse.

                Returns
                -------
                msg_dict : dict
                    The message with items decoded into a dictionary
                """
                msg_dict = super().parse_msg(msg)
                print("Server resposne message = ")
                print(msg_dict)
                msg_dict['result'] = cls.login_result_decoder[msg_dict['result']]
                return msg_dict

    class ChannelInfo:
        class Client(MessageABC):
            pass

        class Server(MessageABC):
            pass
