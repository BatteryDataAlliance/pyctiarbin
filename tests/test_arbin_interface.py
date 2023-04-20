import pytest
from helper_test_utils import Constants, TcpClient
from pycti import ArbinInterface
from pycti.arbinspoofer import ArbinSpoofer
from pycti.messages import Msg

# The channel we will use for testing.
ARBIN_CHANNEL = 13

SPOOFER_CONFIG_DICT = {"ip": "127.0.0.1",
                       "port": 5678,
                       "num_channels": 16}

ARBIN_INTERFACE_CONFIG = {
    "username": "123",
    "password": "123",
    "test_name": "fake_test_name",
    "schedule": "Rest+207855.sdx",
    "channel": ARBIN_CHANNEL+1,
    "arbin_ip": SPOOFER_CONFIG_DICT['ip'],
    "arbin_port": SPOOFER_CONFIG_DICT['port'],
    "timeout_s": 3,
    "msg_buffer_size": 2**12
}

ARBIN_SPOOFER = ArbinSpoofer(SPOOFER_CONFIG_DICT)
ARBIN_SPOOFER.start()


@pytest.mark.arbininterface
def test_start():
    """
    Test that starting the Arbin interface works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())