import pytest
from helper_test_utils import TestClass, msg_packer

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
