import socket
import json
import copy

from pycti.arbinspoofer import ArbinSpoofer

"""
Various parameters we will use accross all the tests.
"""
MSG_BUFFER_SIZE_BYTES = 1024
ARBIN_SPOOFER_CONFIG_DICT = {"ip": "127.0.0.1", 
                             "port": 56278,
                             "num_channels": 16}
CHANNEL = 1  # The channel we will use to associated tests messages.


def __send_recv_msg(s: socket.socket, tx_msg: dict):
    """
    Helper function for sending and receiving messages.

    Parameters
    ----------
    s : socket.socket
        Socket to send and receive with.
    tx_msg : dict
        The message to send.

    Returns
    -------
    rx_msg : dict
        The response msg.
    """
    tx_msg_packed = json.dumps(tx_msg, indent=4).encode()
    s.send(tx_msg_packed)
    rx_msg_packed = s.recv(MSG_BUFFER_SIZE_BYTES)
    rx_msg = json.loads(rx_msg_packed.decode())
    return rx_msg

def test_messages():
    """
    Test that the spoofer replies correctly to all messages.
    """
    spoofer_server = ArbinSpoofer(ARBIN_SPOOFER_CONFIG_DICT)
    spoofer_server.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ARBIN_SPOOFER_CONFIG_DICT["server_ip"], ARBIN_SPOOFER_CONFIG_DICT["json_port"]))

    for tx_msg, ans_key in messages:
        tx_msg['params']['Chan'] = CHANNEL
        ans_key['result']['Chan'] = CHANNEL
        rx_msg = __send_recv_msg(s, tx_msg)
        assert (rx_msg == ans_key)

    s.close()
    spoofer_server.stop()

def test_update_status():
    """
    Check that updating channel status works and does not effect other channel.
    """
    pass