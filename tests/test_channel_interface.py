import pytest
from pyctiarbin import ChannelInterface
from pyctiarbin.arbinspoofer import ArbinSpoofer
from pyctiarbin.messages import Msg

ARBIN_CHANNEL = 1

SPOOFER_CONFIG_DICT = {"ip": "127.0.0.1",
                       "port": 8956,
                       "num_channels": 16}

CHANNEL_INTERFACE_CONFIG = {
    "test_name": "fake_test_name",
    "schedule_name": "Rest+207855.sdx",
    "channel": ARBIN_CHANNEL+1,
    "ip_address": SPOOFER_CONFIG_DICT['ip'],
    "port": SPOOFER_CONFIG_DICT['port'],
    "timeout_s": 3,
    "msg_buffer_size": 2**12
}

ARBIN_SPOOFER = ArbinSpoofer(SPOOFER_CONFIG_DICT)
ARBIN_SPOOFER.start()


@pytest.mark.channel_interface
def test_read_channel_status():
    """
    Test that sending the channel info message works correctly.
    """
    arbin_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
    channel_status = arbin_interface.read_channel_status()

    channel_status_bin_key = Msg.ChannelInfo.Server.pack({'channel': 1})
    channel_status_key = Msg.ChannelInfo.Server.unpack(channel_status_bin_key)
    assert(channel_status == channel_status_key)


@pytest.mark.channel_interface
def test_assign_schedule():
    """
    Test that sending the assign schedule message works correctly.
    """
    arbin_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
    assert(arbin_interface.assign_schedule())


@pytest.mark.channel_interface
def test_start_test():
    """
    Test that sending the start test message works correctly.
    """
    arbin_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
    assert(arbin_interface.start_test())


@pytest.mark.channel_interface
def test_stop_test():
    """
    Test that sending the stop test message works correctly.
    """
    arbin_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
    assert(arbin_interface.stop_test())


@pytest.mark.channel_interface
def test_set_meta_variable():
    """
    Test that assigning schedule  works correctly.
    """
    arbin_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
    assert(arbin_interface.set_meta_variable(mv_num=1, mv_value=4.20))