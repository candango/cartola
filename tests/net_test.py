#!/usr/bin/env python
#
# Copyright 2015-2021 Flavio Garcia
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

"""
Network functions tests
"""

from cartola import net
import unittest
import os
import logging

logger = logging.getLogger(__name__)


class NetworkTestCase(unittest.TestCase):

    def test_valid_host_ping(self):
        """ Test if ping will return true for valid host """
        if os.getenv("NOICMP"):
            logger.warning("ICMP test is disabled, probably it ICMP protocol"
                           "should be blocked in this host.")
        else:
            self.assertTrue(net.ping("github.com"))

    def test_invalid_host_ping(self):
        """ Test if ping will return true for valid host """
        self.assertFalse(net.ping("candngo.org"))

    def test_valid_host_up(self):
        """ Test if host will be up for valid host and port """
        self.assertTrue(net.is_host_up("candango.org", "80"))

    def test_invalid_host_up(self):
        """ Test if host will be up for invalid host and port conbination """
        self.assertFalse(net.is_host_up("candango.org", "8080"))
