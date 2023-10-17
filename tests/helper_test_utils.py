import os
import socket
import json
import struct
from pyctiarbin import MessageABC


class Constants:
    FLOAT_TOLERANCE = 0.0001


class TcpClient():

    msg_buffer_size = 2**12

    def __init__(self, config, retries=5, timeout=1):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.settimeout(timeout)

        connect = False
        retrycnt = retries
        while connect == False and retrycnt > 0:
            try:
                self.__s.connect((config["ip"], config["port"]))
                connect = True
            except socket.timeout:
                print("Connection timed out.")
            except ConnectionRefusedError:
                print("Connection refused.")
            except ConnectionAbortedError:
                print("Connection aborted.")

            if connect == False:
                print("Retrying connection attempt {} of {}.".format(retrycnt, retries))
                retrycnt -= 1

    def send_recv_msg(self, tx_msg) -> bytearray:
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
        rx_msg_length_end_byte = MessageABC.base_template['msg_length']['start_byte'] + struct.calcsize(
            rx_msg_length_format)

        self.__s.sendall(tx_msg)

        rx_msg = b''
        rx_msg += self.__s.recv(self.msg_buffer_size)
        expected_rx_msg_len = struct.unpack(
            rx_msg_length_format, rx_msg[rx_msg_length_start_byte:rx_msg_length_end_byte])[0]
        # Keep reading message in pieces until rx_msg is as long as expected_rx_msg_len
        while len(rx_msg) < expected_rx_msg_len:
            rx_msg += self.__s.recv(self.msg_buffer_size)

        return rx_msg

    def __delete__(self):
        self.__s.close()


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
