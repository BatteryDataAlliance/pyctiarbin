import pytest
import os
import json
import copy
from pycti import Msg

MSG_DIR = os.path.join(os.path.dirname(__file__), 'example_messages')


def message_file_loader(msg_file_name: str) -> tuple:
    '''
    Helper fuction to read in example messages from files.

    Parameters
    ----------
    msg_file_name : str
        The file name the binary and JSON message are saved under

    Returns
    -------
    tuple(bytearray,dict)
        The example message as bytearray and decoded as dict.
    '''
    # Read in the example example binary message
    msg_bin_file_path = os.path.join(
        MSG_DIR, msg_file_name + '.bin')
    with open(msg_bin_file_path, mode='rb') as file:  # b is important -> binary
        msg_bin = file.read()

    # Read in the decoded response message
    msg_decoded_file_path = os.path.join(
        MSG_DIR, msg_file_name + '.json')
    with open(msg_decoded_file_path, mode='r') as file:
        msg_dict = json.load(file)

    return (msg_bin, msg_dict)


@pytest.mark.messages
def test_login_client_msg():
    '''
    Test packing/parsing a client login request messsage
    '''

    example_msg_name = 'client_login_request_msg'
    (msg_bin, msg_dict) = message_file_loader(example_msg_name)

    # Pack the msg_dict and check if it matches the example binary message
    packed_msg = Msg.Login.Client.pack(msg_dict)
    assert (packed_msg == msg_bin)

    # Checking parsing the example message binary and that it matches the msg_dict
    parsed_msg = Msg.Login.Client.parse(msg_bin)
    assert (parsed_msg == msg_dict)


@pytest.mark.messages
def test_login_server_msg():
    '''
    Test parsing/packing a server login response message
    '''
    example_msg_name = 'server_login_response_msg'
    (msg_bin, msg_dict) = message_file_loader(example_msg_name)

    # Check that the parsed binary message mataches the msg_dict
    parsed_msg = Msg.Login.Server.parse(msg_bin)
    assert (parsed_msg == msg_dict)

    # Check packing own version of message from msg_dict
    buildable_msg_dict = copy.deepcopy(msg_dict)
    # Need to re-code this from login_result_decoder
    buildable_msg_dict['result'] = 1
    packed_msg = Msg.Login.Server.pack(buildable_msg_dict)
    parsed_msg = Msg.Login.Server.parse(packed_msg)
    assert (parsed_msg == msg_dict)
