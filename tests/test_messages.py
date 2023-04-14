import pytest
import struct
import os
import json
from pycti import Msg

MSG_DIR = os.path.join(os.path.dirname(__file__), 'example_messages')


@pytest.mark.messages
def test_login_client_msg():
    '''
    Test building/parsing a client login request messsage
    '''
    test_username = 'not a username'
    test_password = 'not a passowrd'

    parsed_msg_ans_key = {
        'header': 1287429013477645789,
        'msg_length': 74,
        'command_code': 4004184065,
        'extended_command_code': 0,
        'username': test_username,
        'password': test_password
    }

    # Generate a independent message to check against
    key_msg = bytearray([])
    key_msg += struct.pack('<Q', parsed_msg_ans_key['header'])
    key_msg += struct.pack('<L', parsed_msg_ans_key['msg_length'])
    key_msg += struct.pack('<L', parsed_msg_ans_key['command_code'])
    key_msg += struct.pack('<L', parsed_msg_ans_key['extended_command_code'])
    key_msg += struct.pack('32s', test_username.encode('ascii'))
    key_msg += struct.pack('32s', test_password.encode('ascii'))
    key_msg += struct.pack('<H', sum(key_msg))

    test_login_cred_dict = {
        'username': test_username,
        'password': test_password
    }
    client_login_msg = Msg.Login.Client.build_msg(test_login_cred_dict)
    assert (client_login_msg == key_msg)

    parsed_client_login_msg = Msg.Login.Client.parse_msg(client_login_msg)
    assert (parsed_client_login_msg == parsed_msg_ans_key)


@pytest.mark.messages
def test_login_server_msg():
    '''
    Test parsing/building a server login response message
    '''

    # Read in the example example binary server response message
    msg_bin_file_path = os.path.join(
        MSG_DIR, 'server_login_response_msg.bin')
    with open(msg_bin_file_path, mode='rb') as file:  # b is important -> binary
        msg_bin = file.read()

    # Read in the decoded response message
    msg_decoded_file_path = os.path.join(
        MSG_DIR, 'server_login_response_msg.json')
    with open(msg_decoded_file_path, mode='r') as file:  # b is important -> binary
        msg_decoded_key = json.load(file)

    # Decode the binary message
    parsed_msg = Msg.Login.Server.parse_msg(msg_bin)

    # Make sure all items in msg_decoded_key match those in parsed message
    for key in msg_decoded_key.keys():
        assert (msg_decoded_key[key] == parsed_msg[key])

    # Check that we create our own version of the message
    built_msg = Msg.Login.Server.build_msg(msg_decoded_key)
    parsed_built_msg = Msg.Login.Server.parse_msg(built_msg)

    # Make sure all items in msg_decoded_key match those in parsed message
    for key in msg_decoded_key.keys():
        assert (msg_decoded_key[key] == parsed_built_msg[key])



