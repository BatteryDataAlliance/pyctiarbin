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


def msg_builder(passed_test_value=None) -> bytearray:
    '''
    Builts bytearray messages independent of MessageABC
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
    Test building a message with MessageAbc.build_msg()
    '''
    key_msg = msg_builder()
    abc_built_msg = TestClass.build_msg()
    assert (abc_built_msg == key_msg)


@pytest.mark.messages
def test_modify_build_msg():
    '''
    Test building a message with MessageAbc.build_msg() and modifying an element in the templet
    '''
    new_test_value = 2.7182

    key_msg = msg_builder(new_test_value)

    update_dict = {'test_value': new_test_value}
    abc_built_msg = TestClass.build_msg(update_dict)
    assert (abc_built_msg == key_msg)


@pytest.mark.messages
def test_modify_build_msg_bad_key():
    '''
    Test building a message with MessageAbc.build_msg() and modifying it with a bad key
    '''
    key_msg = msg_builder()

    update_dict = {'bad_value': 15}
    new_abc_built_msg = TestClass.build_msg(update_dict)
    assert (new_abc_built_msg == key_msg)
