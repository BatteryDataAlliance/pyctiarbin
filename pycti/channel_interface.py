import socket
import logging
import struct
from .messages import Msg
from .messages import MessageABC

from .cycler_interface import CyclerInterface

logger = logging.getLogger(__name__)


class ChannelInterface(CyclerInterface):
    """
    Class for controlling Maccor Cycler using MacNet.
    """

    def __init__(self, config: dict):
        """
        A class for interfacing with the Arbin cycler.

        Parameters
        ----------
        config : dict
            A configuration dictionary.
        """

        # Channels are zero indexed within CTI so we must subtract one here.
        self.__channel = config['channel'] - 1
        self.__config = config

        self.__assign_schedule_feedback = {}
        self.__start_test_feedback = {}
        self.__stop_test_feedback = {}

        super().__init__(self.__config)

    def read_status(self) -> dict:
        """
        Method to read the status of the channel defined in the config.

        Returns
        -------
        status : dict
            A dictionary detailing the status of the channel. Returns None if there is an issue.
        """
        return self.read_channel_status(channel=self.__channel)

    def assign_schedule(self) -> bool:
        """
        Method to assign a schedule to the channel defined in the config.

        Returns
        -------
        success : bool
            True/False based on whether the schedule was assigned without issue.
        """
        success = False

        assign_schedule_msg_tx_bin = Msg.AssignSchedule.Client.pack(
            {'channel': self.__channel, 'schedule': self.__config['schedule']})
        response_msg_bin = self._send_receive_msg(
            assign_schedule_msg_tx_bin)

        if response_msg_bin:
            assign_schedule_msg_rx_dict = Msg.AssignSchedule.Server.unpack(
                response_msg_bin)
            if assign_schedule_msg_rx_dict['result'] == 'success':
                success = True
                logger.info(
                    f'Successfully assigned schedule {self.__config["schedule"]} to channel {self.__config["channel"]}')
            else:
                logger.error(
                    f'Failed to assign schedule {self.__config["schedule"]}! Issue: {assign_schedule_msg_rx_dict["result"]}')
            self.__assign_schedule_feedback = assign_schedule_msg_rx_dict

        return success

    def start_test(self) -> bool:
        """
        Starts channel on method specified in config.  

        Returns
        -------
        success : bool
            True/False based on whether the test was started without issue.
        """
        success = False

        # Make sure the schedule is assigned before starting the test to avoid any funny business
        if self.assign_schedule():
            start_test_msg_tx_bin = Msg.StartSchedule.Client.pack(
                {'channel': self.__channel, 'test_name': self.__config['test_name']})
            response_msg_bin = self._send_receive_msg(
                start_test_msg_tx_bin)

            if response_msg_bin:
                start_test_msg_rx_dict = Msg.StartSchedule.Server.unpack(
                    response_msg_bin)
                if start_test_msg_rx_dict['result'] == 'success':
                    success = True
                    logger.info(
                        f'Successfully started test {self.__config["test_name"]} with schedule {self.__config["schedule"]} on channel {self.__config["channel"]}')
                else:
                    logger.error(
                        f'Failed to start test {self.__config["test_name"]} with schedule {self.__config["schedule"]} on channel {self.__config["channel"]}. Issue: {start_test_msg_rx_dict["result"]}')
                self.__start_test_feedback = start_test_msg_rx_dict

        return success

    def stop_test(self) -> bool:
        """
        Stops the test running on the channel specified in the config.

        Returns
        -------
        success : bool
            True/False based on whether the test stopped without issue.
            Also returns True if no test was running on the channel. 
        """
        success = False

        stop_test_msg_tx_bin = Msg.StopSchedule.Client.pack(
            {'channel': self.__channel})
        response_msg_bin = self._send_receive_msg(
            stop_test_msg_tx_bin)

        if response_msg_bin:
            stop_test_msg_rx_dict = Msg.StopSchedule.Server.unpack(
                response_msg_bin)
            if stop_test_msg_rx_dict['result'] == 'success':
                success = True
                logger.info(
                    f'Successfully stopped test on channel {self.__config["channel"]}')
            else:
                logger.error(
                    f'Failed to stop test on channel {self.__config["channel"]}! Issue: {stop_test_msg_rx_dict["result"]}')
            self.__stop_test_feedback = stop_test_msg_rx_dict

        return success

    def set_meta_variable(self, mv_num: int, mv_value: float) -> bool:
        """
        Sets the passed meta variable number `mv_num` to the passed value `mv_value`
        on the channel specified in the config. Note the test must be running.

        Parameters
        ----------
        mv_num : int
            The meta variable number to set. Must be between 1 and 16 (inclusive)
        mv_value : float
            The meta variable value to set.
        Returns
        -------
        success : bool
            True/False based on whether the meta variable was set. 
        """
        success = False

        updated_msg_vals = {}
        updated_msg_vals['channel'] = self.__channel
        updated_msg_vals['mv_meta_code'] = Msg.SetMetaVariable.Client.mv_channel_codes[mv_num]
        updated_msg_vals['mv_data'] = mv_value

        set_mv_msg_tx_bin = Msg.SetMetaVariable.Client.pack(updated_msg_vals)
        response_msg_bin = self._send_receive_msg(
            set_mv_msg_tx_bin)

        if response_msg_bin:
            set_mv_msg_rx_dict = Msg.SetMetaVariable.Server.unpack(
                response_msg_bin)
            if set_mv_msg_rx_dict['result'] == 'success':
                success = True
                logger.info(
                    f'Successfully set meta variable {mv_num} to a value of {mv_value}')
            else:
                logger.error(
                    f'Failed to set meta variable {mv_num} to a value of {mv_value}! Issue: {set_mv_msg_rx_dict["result"]}')
            self.set_mv_feedback = set_mv_msg_rx_dict

        return success

    def __verify_config(self) -> bool:
        """
        Verifies that the config passed on construction is valid.

        Returns
        --------------------------
        success : bool
            True/False based on whether the config passed at construction is valid.
        """
        required_config_keys = ['username',
                                'password',
                                'test_name',
                                'schedule',
                                'channel',
                                'ip_address',
                                'port',
                                'timeout_s',
                                'msg_buffer_size']

        for key in required_config_keys:
            if key not in self.__config:
                logger.error("Missing key from config! Missing : " + key)
                return False
        logger.info("Config check passed")
        return True