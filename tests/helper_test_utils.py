import os
import json
import struct
from pycti import MessageABC

class TestClass(MessageABC):
    msg_length = 44
    command_code = 0x01

    msg_specific_templet = {
        'test_value': {
            'format': '<f',
            'start_byte': 20,
            'value': 3.14159
        },
        'test_string': {
            'format': '32s',
            'start_byte': 24,
            'text_encoding': 'utf-8',
            'value': 'Test String'
        },
    }

def msg_packer(passed_test_value=None) -> bytearray:
    '''
    Packs bytearray messages independent of MessageABC
    '''

    if passed_test_value:
        test_value = passed_test_value
    else:
        test_value = TestClass.msg_specific_templet['test_value']['value']

    test_string = TestClass.msg_specific_templet['test_string']['value']
    test_string_encoding = TestClass.msg_specific_templet['test_string']['text_encoding']

    key_msg = bytearray([])
    key_msg += struct.pack('<Q', 0x11DDDDDDDDDDDDDD)
    key_msg += struct.pack('<L', TestClass.msg_length)
    key_msg += struct.pack('<L', TestClass.command_code)
    key_msg += struct.pack('<L', 0x00000000)
    key_msg += struct.pack('<f', test_value)
    key_msg += struct.pack('32s', test_string.encode(test_string_encoding))
    key_msg += struct.pack('<H', sum(key_msg))

    return key_msg


def message_file_loader(msg_dir, msg_file_name: str) -> tuple:
    '''
    Helper fuction to read in example messages from files.

    Parameters
    ----------
    msg_dir : str
        The directory containing the example messages.
    msg_file_name : str
        The file name the binary and JSON message are saved under

    Returns
    -------
    tuple(bytearray,dict)
        The example message as bytearray and decoded as dict.
    '''
    # Read in the example example binary message
    msg_bin_file_path = os.path.join(
        msg_dir, msg_file_name + '.bin')
    with open(msg_bin_file_path, mode='rb') as file:  # b is important -> binary
        msg_bin = file.read()

    # Read in the decoded response message
    msg_decoded_file_path = os.path.join(
        msg_dir, msg_file_name + '.json')
    with open(msg_decoded_file_path, mode='r') as file:
        msg_dict = json.load(file)

    return (msg_bin, msg_dict)