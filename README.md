# PyCTI-Arbin

`pycti-arbin` is a Python module that provides cycler and channel level interfaces for communication and control of [Arbin cyclers](https://arbin.com/) via their Console TCP/IP Interface (CTI).

## Overview

- [Motivation](#motivation)
- [Installation](#installation)
  - [Source Installation](#source-installation)
- [Getting Started](#getting-started)
  - [Configuration](#configuration)
    - [CyclerInterface Configuration](#cyclerinterface-configuration)
    - [ChannelInterface Configuration](#channelinterface-configuration)
  - [Env](#env)
- [Getting Channel Readings](#getting-channel-readings)
- [Development](#development)
  - [Contributing](#contributing)
  - [Testing](#testing)
    - [ArbinSpoofer](#arbinspoofer)
  - [Documentation](#documentation)
- [License](#license)

## Motivation

Why did we create `pycti-arbin`? This package enables a wide variety of applications such as:

- Real-time data logging, monitoring and alerting

`pycti-arbin` can be used to passively monitor running tests and log readings directly to a database, bypassing the need to manually export data. Moreover, it's possible to create automated alerts based on incoming real-time data. For example, if a test were to fault or temperature were to exceed a set threshold. While Arbin already has a built-in notification system with MacNotify, `pycti-arbin` provides a more flexible and customizable solution without having to directly modify test procedures.

- Automated test management

The GUI provided by Arbin for test management is straight-forward and easy to use, but requires significant manual work. With `pycti-arbin` it is possible to write programs to automatically start tests simultaneously across many channels (or even many cyclers) at once.

- Testing of next generation closed-loop charging methods

While conventional constant-current followed by constant-voltage (CCCV) charging has been the industry standard for many years and is well supported by cyclers, there is movement towards advanced [closed-loop control charging techniques that provide improved battery life and decreased charge times](https://battgenie.life/technology/). `pycti-arbin` enables testing of closed-loop battery charging methods by providing an interface between software hosting battery charging algorithms and active Arbin tests, allowing the charge current to be dynamically set.

- Well tested, easy to use, community supported interface in the most popular programming language.

It is entirely possible to write one's own CTI wrapper, but `pycti-arbin` provides a well-tested ready to use package that takes care of lower level communication, providing a simple yet powerful interface in the most popular programming language.

## Installation

### Using pip

`pycti-arbin` can be installed using pip:

```bash
pip install pycti-arbin
```

### Source Installation

To install from source, type the following into the command line:

```bash
git clone https://github.com/BattGenie/pycti.git
cd pycti
pip install -r requirements.txt
pip install .
```

## Getting Started

`pycti-arbin` provides two distinct classes for interacting with Arbin cyclers:

- `CyclerInterface` : A cycler-level interface for reading channel status of any channel on the cycler. This class is capable of read only operations on the cycler.

- `ChannelInterface` : A channel-level interface for reading status of a specific channel, starting/stopping tests on that channel, and assigning meta variables during active tests on the channel. This class is capable of read and write operations on a single channel.

### Configuration

Both `CyclerInterface` and `ChannelInterface` require configuration dictionaries upon initialization. The fields of these configuration dictionaries are detailed in the following sections.

#### CyclerInterface Configuration

An example `CyclerInterface` configuration dictionary is shown below:

```python
CYCLER_INTERFACE_CONFIG = {
    "ip_address": 127.0.0.1,
    "port": 1234,
    "timeout_s": 3,
    "msg_buffer_size": 4096
}
```

Where the fields are as follows:

- `ip_address` : str
    The IP address of the Arbin host computer.
- `port` : int
    The TCP port to communicate through. This is generally going to be 9031
- `timeout_s` : *optional* : float
    How long to wait before timing out on TCP communication. Defaults to 3 seconds.
- `msg_buffer_size` : *optional* : int
    How big of a message buffer to use for sending/receiving messages.
    A minimum of 1024 bytes is recommended. Defaults to 4096 bytes.

#### ChannelInterface Configuration

An example `ChannelInterface` configuration dictionary is shown below:

```python
CHANNEL_INTERFACE_CONFIG = {
  "channel": 1,
  "test_name": "fake_test_name",
  "schedule_name": "Rest+207855.sdx",
  "ip_address": 127.0.0.1,
  "port": 1234,
  "timeout_s": 3,
  "msg_buffer_size": 4096
}
```

Where the fields are as follows:

- `channel` : int
    The channel to target with the ChannelInterface class instance.
- `test_name` : *optional* : str
    The test name to use if using the ChannelInterface to start a test.
- `schedule_name` : *optional* : str
    The name of the schedule file to use if using the ChannelInterface to start a test.
- `ip_address` : str
    The IP address of the Arbin host computer.
- `port` : int
    The TCP port to communicate through. This is generally going to be 7031
- `timeout_s` : *optional* : float
    How long to wait before timing out on TCP communication. Defaults to 3 seconds.
- `msg_buffer_size` : *optional* : int
    How big of a message buffer to use for sending/receiving messages.
    A minimum of 1024 bytes is recommended. Defaults to 4096 bytes.

### Env

In addition to a configuration dictionary, both interfaces require a `.env` file containing the Arbin CTI username and password to use for communication. The `.env` file path can be passed as a constructor argument. If it is not specified, the the program looks in the working directly for a `.env` file.

The `.env` file must contain the following fields:

```bash
ARBIN_CTI_USERNAME='your_username'
ARBIN_CTI_PASSWORD='your_password'
```

Where `your_username` and `your_password` should be replaced with your username and password.

### Getting Channel Readings

To get channel readings with a `CyclerInterface` you must specify which channel you want to read from:

```python
from pyctiarbin import CyclerInterface

CYCLER_INTERFACE_CONFIG = {
    "ip_address": "127.0.0.1"
    "port": 1234,
    "timeout_s": 3,
    "msg_buffer_size": 4096
}

cycler_interface = CyclerInterface(CYCLER_INTERFACE_CONFIG)
cycler_interface.read_channel_status(channel=1)
```

For a `ChannelInterface` there is no need to specify the channel since we define it in the config:

```python
from pyctiarbin import ChannelInterface

CHANNEL_INTERFACE_CONFIG = {
  "channel": 1,
  "test_name": "fake_test_name",
  "schedule_name": "Rest+207855.sdx",
  "ip_address": "127.0.0.1"
  "port": 1234,
  "timeout_s": 3,
  "msg_buffer_size": 4096
}

channel_interface = ChannelInterface(CHANNEL_INTERFACE_CONFIG)
channel_interface.read_channel_status()
```

For more examples of how to use the `CyclerInterface` and `ChannelInterface` class see the `demo_notebook.ipynb` and documentation.

## Tested MITS Pro Version

| Version         | Build      | pycti-arbin |
|-----------------|------------|-------------|
| Mits8 PV.202110 | Oct 4 2021 | 0.0.4       |
|                 |            |             |

## Development

This section contains various information to help developers further extend and test `pycti-arbin`

## Contributing

As it exists now `pycti-arbin` only implements a fraction of the messages supported by CTI. Further work can be done to expand `pycti-arbin` to include more of the messages detailed in the CTI documentation `docs/ArbinCTI_Protocol v1.1.pdf`.

We welcome your help in expanding `pycti-arbin`! Please see the [CONTRIBUTING.md](https://github.com/BattGenie/pycti/blob/main/CONTRIBUTING.md) file in this repository for contribution guidelines.

## Testing

To run the tests navigate to the "tests" directory and type the following:

```bash
pytest .
```

To run tests and generate a coverage report:

```bash
coverage run -m pytest
```

To view the generated coverage report:

```bash
coverage report -m 
```

### ArbinSpoofer

Testing software on a real cycler is dangerous so we've created a submodule `arbinspoofer` to emulate some of the behavior of the Arbin software with a class `ArbinSpoofer`. This class creates a local TCP server and that accepts connections from n number of clients. The `ArbinSpoofer` does not perfectly emulate a Arbin cycler (for example, it does not track if a test is already running on a channel) and merely checks that the message format is correct and responds with standard messages.

## Documentation

All documentation was generated with [pydoc](https://docs.python.org/3/library/pydoc.html). To re-generate the documentation type the following command from the top level directory of the repository:

```bash
pydoc --html .
```

## License

MIT License

Copyright (c) 2023 BattGenie Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
