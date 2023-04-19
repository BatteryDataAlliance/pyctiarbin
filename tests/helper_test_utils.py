import os
import json

class Constants:
    FLOAT_TOLERANCE = 0.0001

def message_file_loader(msg_dir, msg_file_name: str) -> tuple:
    '''
    Helper function to read in example messages from files.

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

def aux_dict_builder() -> dict:
    msg_dict = {}
    msg_dict['aux_voltage_count'] = 0
    msg_dict['aux_temperature_count'] = 0
    msg_dict['aux_pressure_count'] = 0
    msg_dict['aux_external_count'] = 0
    msg_dict['aux_flow_count'] = 0
    msg_dict['aux_ao_count'] = 0
    msg_dict['aux_di_count'] = 0
    msg_dict['aux_do_count'] = 0
    msg_dict['aux_safety_count'] = 0
    msg_dict['aux_humidity_count'] = 0
    msg_dict['aux_ph_count'] = 0
    msg_dict['aux_density_count'] = 0

    return msg_dict
