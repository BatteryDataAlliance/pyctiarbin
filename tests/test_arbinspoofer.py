import socket
import struct
from helper_test_utils import Constants
from pycti.arbinspoofer import  ArbinSpoofer
from pycti.messages import Msg, MessageABC


"""
Various parameters we will use across all the tests.
"""
MSG_BUFFER_SIZE_BYTES = 2**12
CONFIG_DICT = {"ip": "127.0.0.1",
               "port": 5678,
               "num_channels": 16}
CHANNEL = 5  # The channel we will use to associated tests messages.


def __send_recv_msg(s: socket.socket, tx_msg: bytearray) -> bytearray:
    """
    Helper function for sending and receiving messages.

    Parameters
    ----------
    s : socket.socket
        Socket to send and receive with.
    tx_msg : bytearray
        The message to send.

    Returns
    -------
    rx_msg : dict
        The response msg.
    """

    rx_msg_length_format = MessageABC.base_template['msg_length']['format']
    rx_msg_length_start_byte = MessageABC.base_template['msg_length']['start_byte']
    rx_msg_length_end_byte = MessageABC.base_template['msg_length']['start_byte'] + struct.calcsize(rx_msg_length_format)

    s.sendall(tx_msg)

    rx_msg = b''
    rx_msg += s.recv(MSG_BUFFER_SIZE_BYTES)
    expected_rx_msg_len = struct.unpack(
        rx_msg_length_format, rx_msg[rx_msg_length_start_byte:rx_msg_length_end_byte])[0]
    # Keep reading message in pieces until rx_msg is as long as expected_rx_msg_len
    while len(rx_msg) < expected_rx_msg_len:
        rx_msg += s.recv(MSG_BUFFER_SIZE_BYTES)

    return rx_msg


def test_messages():
    """
    Test that the spoofer replies correctly to all messages.
    """
    arbin_spoofer = ArbinSpoofer(CONFIG_DICT)
    arbin_spoofer.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CONFIG_DICT["ip"], CONFIG_DICT["port"]))    
    
    # Send all messages and make sure we get the correct responses.
    messages = [(Msg.Login.Client.pack(), Msg.Login.Server.pack()),
                (Msg.ChannelInfo.Client.pack(), Msg.ChannelInfo.Server.pack()),
                (Msg.AssignSchedule.Client.pack(), Msg.AssignSchedule.Server.pack()),
                (Msg.StartSchedule.Client.pack(), Msg.StartSchedule.Server.pack()),
                (Msg.StopSchedule.Client.pack(), Msg.StopSchedule.Server.pack()),
                (Msg.SetMetaVariable.Client.pack(), Msg.SetMetaVariable.Server.pack()),
                ]

    for tx_msg, expected_rx_msg in messages:
        rx_msg = __send_recv_msg(s, tx_msg)
        assert (rx_msg == expected_rx_msg)

    s.close()
    arbin_spoofer.stop()


def test_update_status():
    """
    Check that updating channel status works and does not effect other channel.
    """

    arbin_spoofer = ArbinSpoofer(CONFIG_DICT)
    arbin_spoofer.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CONFIG_DICT["ip"], CONFIG_DICT["port"]))    

    # Check initial channel readings 
    tx_msg = Msg.ChannelInfo.Client.pack({'channel':CHANNEL})
    rx_msg = __send_recv_msg(s, tx_msg)
    # Generate the message we would expect to get back
    rx_msg_expected = Msg.ChannelInfo.Server.pack({'channel':CHANNEL})
    assert(rx_msg==rx_msg_expected)

    # Now check updating the values 
    updated_readings = {'voltage_v':2.69, 'current_a':1.19}
    arbin_spoofer.update_channel_status(CHANNEL, updated_readings)
    rx_msg = __send_recv_msg(s, tx_msg)
     # Generate the message we would expect to get back
    rx_msg_expected = Msg.ChannelInfo.Server.pack({**{'channel':CHANNEL},**updated_readings})
    # Check it in binary
    assert(rx_msg==rx_msg_expected)

    rx_msg_dict = Msg.ChannelInfo.Server.unpack(rx_msg)

    # Now check it unpacked 
    # Check that aux readings were assigned correctly
    assert (abs(updated_readings['voltage_v'] - rx_msg_dict['voltage_v'])
            < Constants.FLOAT_TOLERANCE)
    assert (abs(updated_readings['current_a'] - rx_msg_dict['current_a'])
            < Constants.FLOAT_TOLERANCE)

    s.close()
    arbin_spoofer.stop()