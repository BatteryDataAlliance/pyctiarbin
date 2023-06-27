# pycti

`pytcti` is a Python module that provides a channel level interface for communication and control of [Arbin cyclers](https://arbin.com/) via their Console TCP/IP Interface (CTI). `pycti` provides a hassle-free way to utilize CTI with a simple Python class.

### Overview

- [Motivation](#Motivation)
- [Installation](#Installation)
    - [Requirements](#Requirements)
    - [Source Installation](#source-installation)
- [CTI Message Anatomy]
- [Examples](#Examples)
  - [Getting Started](#getting-started)
    - [Configuration](#Configuration)
  - [Getting Channel Readings](#getting-channel-readings) 
  - [Starting a Test](#starting-a-test)
  - [Setting Variables](#setting-variables)
- [Development](#Dev)
  - [Contributing](#Contributing)
  - [Testing](#Testing)
    - [MaccorSpoofer](#MaccorSpoofer)
  - [Documentation](#Documentation)
- [License](#License)

# <a name="Motivation"></a>Motivation

Why did we create `pycti`? This package enables a wide variety of applications such as:

- Real-time data logging, monitoring and alerting

`pycti` can be used to passively monitor running tests and log readings directly to a database, bypassing the need to manually export data. Moreover, it's possible to create automated alerts based on incoming real-time data. For example, if a test were to fault or temperature were to exceed a set threshold. While Arbin already has a built-in notification system with MacNotify, `pycti` provides a more flexible and customizable solution without having to directly modify test procedures. 

- Automated test management

The GUI provided by Arbin for test management is straight-forward and easy to use, but requires significant manual work. With `pycti` it is possible to write programs to automatically start tests simultaneously across many channels (or even many cyclers) at once.

- Testing of next generation closed-loop charging methods

While conventional constant-current followed by constant-voltage (CCCV) charging has been the industry standard for many years and is well supported by cyclers, there is movement towards advanced [closed-loop control charging techniques that provide improved battery life and decreased charge times](https://battgenie.life/technology/). `pycti` enables testing of closed-loop battery charging methods by providing an interface between software hosting battery charging algorithms and active Arbin tests, allowing the charge current to be dynamically set.

- Well tested, easy to use, community supported interface in the most popular programming language. 

It is entirely possible to write one's own CTI wrapper, but `pycti` provides a well-tested ready to use package that takes care of lower level communication, providing a simple yet powerful interface in the most popular programming language. 

# <a name="Installation"></a>Installation

## <a name="Requirements"></a>Requirements

`pycti` requires only Python 3 and packages from the standard library. It has been tested on on Windows, Mac, and Debian operating systems.

## <a name="Source Installation"></a>Source Installation

To install from source clone [this repository](https://github.com/BattGenie/pycti), navigate into the directory, and type the following into the command line:

```
pip install .
```

# <a name="Examples"></a>Examples

## <a name="Getting Started"></a>Getting Started

`pycti` provides a class `ArbinInterface` that communicates with the Arbin cycler via CTI. Each class instance targets a specific channel of the cycler and requires a configuration dictionary with the following fields:

### <a name="Configuration"></a>Configuration

- `username` - The username to login to the Arbin server.
- `password` - The password to login to the Arbin server.
- `channel` - The channel to be targeted for all operations.
- `test_name` - The test name to be used for any tests started. If left blank, Arbin will generate a unique random name for any started tests. Note that Arbin requires unique test names for each test.
- `schedule` - The schedule to use for testing.
- `test_schedule` - The test procedure to be used, if starting a test with a procedure. Not needed with direct control.
- `ip_address` - The IP address of the Arbin server. Use 127.0.0.1 if running on the same machine as the server.
- `port` - The port to TCP/IP port to communicate through.
- `timeout_s` - How long to wait on Arbin messages before giving a timeout error.
- `msg_buffer_size` - How large of a message buffer size to use.

## <a name="Readings"></a>Getting Channel Readings

## <a name="Test"></a>Starting a Test

# <a name="Dev"></a>Development

This section contains various information to help developers further extend and test `pycti`

## <a name="Contributing"></a>Contributing

As it exists now `pycti` only implements a fraction of the messages supported by CTI. Further work can be done to expand `pycti` to include more of the messages detailed in the CTI documentation `docs/ArbinCTI_Protocol v1.1.pdf`.

We welcome your help in expanding `pycti`! Please see the [CONTRIBUTING.md](https://github.com/BattGenie/pycti/blob/main/CONTRIBUTING.md) file in this repository for contribution guidelines. 

## <a name="Testing"></a>Testing

To run the tests navigate to the "tests" directory and type the following:

```
pytest .
```

To run tests and generate a coverage report:

```
coverage run -m pytest
```

To view the generated coverage report:

```
coverage report -m 
```

### <a name="ArbinSpoofer"></a>MaccorSpoofer

Testing software on a real cycler is dangerous so we've created a submodule `arbinspoofer` to emulate some of the behavior of the Arbin software with a class `ArbinSpoofer`. This class creates a local TCP server and that accepts connections from n number of clients. The `ArbinSpoofer` does not perfectly emulate a Arbin cycler (for example, it does not track if a test is already running on a channel) and merely checks that the message format is correct and responds with standard messages. 

## <a name="Documentation"></a>Documentation

All documentation was generated with [pydoc](https://docs.python.org/3/library/pydoc.html). To re-generate the documentation type the following command from the top level directory of the repository:

```
pdoc --html .
```

# <a name="License"></a>License

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
