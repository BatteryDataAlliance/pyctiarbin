import pytest
import os
import copy
import struct
from pycti import Msg
from helper_test_utils import Constants, message_file_loader, aux_dict_builder

MSG_DIR = os.path.join(os.path.dirname(__file__), 'example_messages')


@pytest.mark.messages
def test_aux_readings_parser_no_aux():
    '''
    Test that the aux_readings_parser works correctly with no aux readings
    '''
    msg_dict = aux_dict_builder()
    msg_bin = bytearray([])
    msg_dict = Msg.ChannelInfo.Server.aux_readings_parser(msg_dict, msg_bin, 0)
    for key in msg_dict.keys():
        if not key.endswith('_count'):
            assert (len(msg_dict[key]) == 0)


@pytest.mark.messages
def test_aux_readings_parser_voltage_and_temp():
    '''
    Test that the aux_readings_parser works correctly with voltage and temperature readings
    '''
    msg_dict = aux_dict_builder()
    msg_dict['aux_voltage_count'] = 2
    msg_dict['aux_temperature_count'] = 1

    aux_voltage_1 = 1.0
    aux_voltage_dt_1 = 0.1
    aux_voltage_2 = 2.0
    aux_voltage_dt_2 = 0.2
    aux_temperature_1 = 3.0
    aux_temperature_dt_1 = 0.3

    msg_bin = bytearray([])
    msg_bin += struct.pack('<f', aux_voltage_1)
    msg_bin += struct.pack('<f', aux_voltage_dt_1)
    msg_bin += struct.pack('<f', aux_voltage_2)
    msg_bin += struct.pack('<f', aux_voltage_dt_2)
    msg_bin += struct.pack('<f', aux_temperature_1)
    msg_bin += struct.pack('<f', aux_temperature_dt_1)

    msg_dict = Msg.ChannelInfo.Server.aux_readings_parser(msg_dict, msg_bin, 0)

    # Check that aux readings were assigned correctly
    assert (abs(msg_dict['aux_voltages'][0] - aux_voltage_1)
            < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_voltages_dt'][0] -
            aux_voltage_dt_1) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_voltages'][1] - aux_voltage_2)
            < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_voltages_dt'][1] -
            aux_voltage_dt_2) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_temperatures'][0] -
            aux_temperature_1) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_temperatures_dt'][0] -
            aux_temperature_dt_1) < Constants.FLOAT_TOLERANCE)


@pytest.mark.messages
def test_aux_readings_parser_only_temp():
    '''
    Test that the aux_readings_parser works correctly with only temperature readings
    '''

    # # Now check that we can prase voltage and temperature aux readings
    msg_dict = aux_dict_builder()
    msg_dict['aux_temperature_count'] = 2

    aux_temperature_1 = 3.0
    aux_temperature_dt_1 = 0.3
    aux_temperature_2 = 4.0
    aux_temperature_dt_2 = 0.4

    msg_bin = bytearray([])
    msg_bin += struct.pack('<f', aux_temperature_1)
    msg_bin += struct.pack('<f', aux_temperature_dt_1)
    msg_bin += struct.pack('<f', aux_temperature_2)
    msg_bin += struct.pack('<f', aux_temperature_dt_2)

    msg_dict = Msg.ChannelInfo.Server.aux_readings_parser(msg_dict, msg_bin, 0)

    # Check that aux readings were assigned correctly
    assert (abs(msg_dict['aux_temperatures'][0] -
            aux_temperature_1) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_temperatures_dt'][0] -
            aux_temperature_dt_1) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_temperatures'][1] -
            aux_temperature_2) < Constants.FLOAT_TOLERANCE)
    assert (abs(msg_dict['aux_temperatures_dt'][1] -
            aux_temperature_dt_2) < Constants.FLOAT_TOLERANCE)
