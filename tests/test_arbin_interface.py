import pytest
from pycti import ArbinInterface
from pycti.arbinspoofer import ArbinSpoofer
from pycti.messages import Msg

ARBIN_CHANNEL = 1

SPOOFER_CONFIG_DICT = {"ip": "127.0.0.1",
                       "port": 8956,
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


@pytest.mark.arbininterface
def test_read_status():
    """
    Test that sending the channel info message works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())
    channel_status = arbin_interface.read_status()

    channel_status_bin_key = Msg.ChannelInfo.Server.pack({'channel': 1})
    channel_status_key = Msg.ChannelInfo.Server.unpack(channel_status_bin_key)
    assert(channel_status == channel_status_key)


@pytest.mark.arbininterface
def test_assign_schedule():
    """
    Test that sending the assign schedule message works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())
    assert(arbin_interface.assign_schedule())


@pytest.mark.arbininterface
def test_start_test():
    """
    Test that sending the start test message works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())
    assert(arbin_interface.start_test())


@pytest.mark.arbininterface
def test_stop_test():
    """
    Test that sending the stop test message works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())
    assert(arbin_interface.stop_test())


@pytest.mark.arbininterface
def test_set_meta_variable():
    """
    Test that assigning schedule  works correctly.
    """
    arbin_interface = ArbinInterface(ARBIN_INTERFACE_CONFIG)
    assert(arbin_interface.start())
    assert(arbin_interface.set_meta_variable(mv_num=1, mv_value=4.20))