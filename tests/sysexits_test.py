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
Datetime tests
"""

from cartola import sysexits
import unittest


class SysexitsTestCase(unittest.TestCase):

    def test_exit(self):
        """ Testing if the system exit will return the provided code."""
        with self.assertRaises(SystemExit) as arc:
            sysexits.exit(sysexits.EX_BASE)
        self.assertEqual(sysexits.EX_BASE, arc.exception.code)

    def test_exit_fatal(self):
        """ Testing if the system exit will return the provided code plus the
        fatal error."""
        code = 15
        with self.assertRaises(SystemExit) as arc:
            sysexits.exit_fatal(code)
        self.assertEqual(sysexits.EX_FATAL_ERROR + code, arc.exception.code)
