import pytest
import os
import copy
from pyctiarbin import Msg
from helper_test_utils import message_file_loader

MSG_DIR = os.path.join(os.path.dirname(__file__), 'example_messages')

@pytest.mark.messages
def test_login_client_msg():
    '''
    Test packing/parsing a client login request message
    '''

    example_msg_name = 'client_login_msg'
    (msg_bin, msg_dict) = message_file_loader(MSG_DIR, example_msg_name)

    # Pack the msg_dict and check if it matches the example binary message
    packed_msg = Msg.Login.Client.pack(msg_dict)
    assert (packed_msg == msg_bin)

    # Checking parsing the example message binary and that it matches the msg_dict
    parsed_msg = Msg.Login.Client.unpack(msg_bin)
    assert (parsed_msg == msg_dict)


@pytest.mark.messages
def test_login_server_msg():
    '''
    Test parsing/packing a server login response message
    '''
    example_msg_name = 'server_login_msg'
    (msg_bin, msg_dict) = message_file_loader(MSG_DIR, example_msg_name)

    # Check that the parsed binary message matches the msg_dict
    parsed_msg = Msg.Login.Server.unpack(msg_bin)
    assert (parsed_msg == msg_dict)

    # Check packing own version of message from msg_dict
    buildable_msg_dict = copy.deepcopy(msg_dict)
    # Need to re-code this from login_result_decoder
    buildable_msg_dict['result'] = 1
    packed_msg = Msg.Login.Server.pack(buildable_msg_dict)
    parsed_msg = Msg.Login.Server.unpack(packed_msg)
    assert (parsed_msg == msg_dict)
