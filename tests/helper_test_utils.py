import os
import json


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
