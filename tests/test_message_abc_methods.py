import pytest
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


@pytest.mark.messages
def test_simple_build_msg():
    '''
    Test packing a message with MessageAbc.pack()
    '''
    key_msg = msg_packer()
    abc_built_msg = TestClass.pack()
    assert (abc_built_msg == key_msg)


@pytest.mark.messages
def test_modify_build_msg():
    '''
    Test packing a message with MessageAbc.pack() and modifying an element in the templet
    '''
    new_test_value = 2.7182

    key_msg = msg_packer(new_test_value)

    update_dict = {'test_value': new_test_value}
    abc_built_msg = TestClass.pack(update_dict)
    assert (abc_built_msg == key_msg)


@pytest.mark.messages
def test_modify_build_msg_bad_key():
    '''
    Test packing a message with MessageAbc.pack() and modifying it with a bad key
    '''
    key_msg = msg_packer()

    update_dict = {'bad_value': 15}
    new_abc_built_msg = TestClass.pack(update_dict)
    assert (new_abc_built_msg == key_msg)


@pytest.mark.messages
def test_modify_build_bad_pack():
    '''
    Test packing a message with MessageAbc.pack() but with an item that will fail packing
    '''
    # We should get back an empty message
    key_msg = bytearray([])

    update_dict = {'command_code': 'this should not be a string'}
    new_abc_built_msg = TestClass.pack(update_dict)
    assert (new_abc_built_msg == key_msg)


@pytest.mark.messages
def test_parse_msg():
    '''
    Test pasrsing a message with MessageAbc.parse()
    '''
    ans_key_dict = {
        'header': 1287429013477645789,
        'msg_length': 44,
        'command_code': 1,
        'extended_command_code': 0,
        'test_value': 3.141590118408203,
        'test_string': 'Test String'
    }

    # Prase the message
    key_msg = msg_packer()
    prased_msg_dict = TestClass.parse(key_msg)

    for key in ans_key_dict.keys():
        assert (ans_key_dict[key] == prased_msg_dict[key])
