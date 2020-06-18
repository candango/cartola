#!/usr/bin/env python
#
# Copyright 2015-2019 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import platform
from socket import AF_INET, SOCK_STREAM, socket
import subprocess


logger = logging.getLogger(__name__)

TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURES_ROOT = os.path.join(TEST_ROOT, "fixtures")
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_ROOT, ".."))


def is_host_up(host, port):
    """
    See: https://bit.ly/2BgCpHI
    :param host:
    :param port:
    :return:
    """
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((host, int(port)))
    if result == 0:
        s.close()
        return True
    elif result == 10035:
        logger.warning("Timeout reached")
    else:
        logger.warning("Connection closed")
    s.close()
    return False


def ping(host):
    """ Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the
    host name is valid.
    Base on https://bit.ly/2TmgeX2 but with pexpect
    :param str host: A host name or ip
    :return boolean: True if ping is replied correctly
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Building the command. Ex: "ping -c 1 example.com"
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0
