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

from cartola import dt
import unittest


class DtTestCase(unittest.TestCase):

    def test_extract_datetime(self):
        """ Last extract datetime from a string tests"""
        self.assertEqual("01", dt.complete_month(2020, 1))
        self.assertEqual("08", dt.complete_month(2020, 8))
        self.assertEqual("11", dt.complete_month(2020, 11))

    def test_last_day_of_month(self):
        """ Last day of month tests"""
        self.assertEqual(dt.last_day_of_month(2020, 2), 29)
        self.assertEqual(dt.last_day_of_month(2020, 9), 30)
        self.assertEqual(dt.last_day_of_month(2020, 10), 31)
