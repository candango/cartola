#!/usr/bin/env python
#
# Copyright 2015-2022 Flavio Garcia
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
import unittest
from tests import (config_test, dt_test, exception_test, fs_test, ftext_test,
                   net_test, pagination_test, security_test, sysexits_test,
                   xray_test)

logger = logging.getLogger(__name__)


def suite():
    testLoader = unittest.TestLoader()
    alltests = unittest.TestSuite()
    alltests.addTests(testLoader.loadTestsFromModule(config_test))
    alltests.addTests(testLoader.loadTestsFromModule(dt_test))
    alltests.addTests(testLoader.loadTestsFromModule(exception_test))
    alltests.addTests(testLoader.loadTestsFromModule(fs_test))
    alltests.addTests(testLoader.loadTestsFromModule(ftext_test))
    if os.getenv("NOICMP"):
        logger.warning("NOICMP environment variable suppressing net_test case."
                       " Probably the ICMP protocol is blocked in this host.")
    else:
        alltests.addTests(testLoader.loadTestsFromModule(net_test))
    alltests.addTests(testLoader.loadTestsFromModule(pagination_test))
    alltests.addTests(testLoader.loadTestsFromModule(security_test))
    alltests.addTests(testLoader.loadTestsFromModule(sysexits_test))
    alltests.addTests(testLoader.loadTestsFromModule(xray_test))
    return alltests


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite())
    if not result.wasSuccessful():
        exit(2)
