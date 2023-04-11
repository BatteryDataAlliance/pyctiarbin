import socket
import json
import threading
import copy

class ChannelData:

    __chan_status_list = []
    __chan_status_lock = threading.Lock()

    def __init__(self, num_channels):
        """
        Container class that will hold all of the specific channel data for MaccorSpoofer.

        Parameters
        ----------
            num_channels : int
                Number of channels in our hypothetical Maccor cycler.
        """
        self.num_channels = num_channels

    def fetch_channel_status(self, channel) -> dict:
        """
        Returns the status message for a specified channel.

        Parameters
        ----------
        channel : int
            The channel to return the status for.

        Returns
        -------
        status : dict
            The status message for the requested channel. Empty if channel larger than number of channel
        """
        return {}

    def update_channel_status(self, channel, updated_status):
        """
        Updates the stored channel status for the specified channel.

        Parameters
        ----------
        channel : int
            The channel to update the status for.
        updated_status : dict
            Complete or partial dictionary of status values to update.

        Returns
        -------
        success : bool
            Returns True if all values in the updated_status were used to update the channel_status_array.
        """
        return False


class ArbinSpoofer:

    __client_connect_timeout_s = 1
    __stop_servers_lock = threading.Lock()
    __stop_servers = False

    def __init__(self, config: dict):
        """
        Class to mimic behavior of Arbin cycler MITSPro control server. The class is currently dumb 
        and just sends back basic response messages without any notion of channel status or readings. 
        It could be expanded in future. 

        Parameters
        ----------
        config : dict
            A configuration dictionary containing the following fields:

            `ip`: The server IP address to host from. Most often 'localhost' for testing.

            `port`: The port to use for the JSON server.

            `num_channels`: The number of channel our fictional cycler has.
        """

        self.__channel_data = ChannelData(config['num_channels'])

        self.__server_thread = threading.Thread(
            target=self.__server_loop,
            args=(config, _TcpWorker,),
            daemon=True
        )

    def start(self):
        """
        Starts the server loops.
        """
        self.__server_thread.start()

    def update_channel_status(self, channel, updated_status):
        """
        Updates the stored channel status for the specified channel.

        Parameters
        ----------
        channel : int
            The channel to update the status for.
        updated_status : dict
            Complete or partial dictionary of status values to update.

        Returns
        -------
        success : bool
            Returns True if all values in the updated_status were used to update the channel_status_array.
        """
        return self.__channel_data.update_channel_status(channel, updated_status)

    def __server_loop(self, sock_config: dict, Worker):
        """
        Creates a server and forever loop to service client socket requests.

        Parameters
        ----------
        sock_cofig : dict
            A configuration for the socket containing the IP and port number.
        Worker : _SocketWorker
            A reference to the worker class that will service individual client connections.
        """
        # List that will hold all the workers to service client connections.
        client_workers = []

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((sock_config["ip"], sock_config["port"]))
        sock.settimeout(self.__client_connect_timeout_s)
        sock.listen()

        while True:
            try:
                client_connection = sock.accept()[0]
                client_workers.append(
                    Worker(client_connection, self.__channel_data))
            except socket.timeout:
                with self.__stop_servers_lock:
                    # If stop commmand is issued then kill all workers.
                    if self.__stop_servers:
                        for worker in client_workers:
                            if worker.is_alive():
                                worker.kill_worker()
                        break
                # Remove any workers that made have died from disconnecting clients.
                client_workers[:] = [
                    worker for worker in client_workers if worker.is_alive()
                ]

    def stop(self):
        """
        Stop the server loops.
        """
        with self.__stop_servers_lock:
            self.__stop_servers = True
        self.__server_thread.join()

    def __del__(self):
        self.stop()


class _SocketWorker:
    """
    Generic worker class that will respond to client socket requests. 
    Default setup as an echo server. Child classes should overwrite the 
    the `_process_client_msg()` method with their own responses.
    """
    __receive_msg_timeout_s = 1
    __msg_buffer_size_bytes = 1024
    __stop_lock = threading.Lock()
    __stop = False

    def __init__(self, s: socket.socket):
        """
        Creates the thread to service client requests.

        Parameters
        ----------
        s : socket.socket
            Socket connection to client.
        """
        self.stop = False
        self.__client_thread = threading.Thread(
            target=self.___service_loop,
            args=(s,),
            daemon=True
        )
        self.__client_thread.start()

    def ___service_loop(self, s: socket.socket):
        """
        Forever loop to service client requests. Wait to receive a message. If no messages is 
        received before the timeout then check to see if stop command has been issued. Loop is 
        also broken if client breaks conenction by sending b''. 

        Parameters
        ----------
        s : socket.socket
            Socket connection to client.
        """
        s.settimeout(self.__receive_msg_timeout_s)

        while True:
            try:
                rx_msg = s.recv(self.__msg_buffer_size_bytes)
                if not rx_msg:
                    break
                tx_msg = self._process_client_msg(rx_msg)
                s.sendall(tx_msg)
            except socket.timeout:
                with self.__stop_lock:
                    if self.__stop:
                        break
        s.close()

    def _process_client_msg(self, rx_msg):
        """
        Takes the incoming client message and generates a response. 

        Parameters
        ----------
        rx_msg : PyBytesObject
            The client message received.

        Returns
        -------
        tx_msg : PyBytesObject
            The client response.
        """
        return rx_msg

    def is_alive(self):
        """
        Method to call to see if the client service thread is still running.

        Returns
        -------
        running : bool
            True of False based on whether or not the client thread is running.
        """
        return self.__client_thread.is_alive()

    def kill_worker(self):
        """
        Method to stop client service loop.
        """
        if self.__client_thread.is_alive():
            with self.__stop_lock:
                self.__stop = True
            self.__client_thread.join()

class _TcpWorker(_SocketWorker):

    def __init__(self, s: socket.socket, channel_data: ChannelData):
        """
        Class to handle requests from MacNet TCP socket clients. Currently just echos back client
        message. Should be expanded in future.

        Parameters
        ----------
        s : socket.socket
            Socket to communicate with.
        channel_data : ChannelData
            Container class of channel data
        """

        self.__channel_data = channel_data
        super().__init__(s)
