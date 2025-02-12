#!/usr/bin/env python
#
# Copyright 2015-2025 Flavio Garcia
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
Security tests
"""

from cartola.security import random_string
import unittest


class RandomStringTestCase(unittest.TestCase):

    def test_random_string(self):
        """ Random string generation """
        self.assertNotEqual(random_string(), None)
        self.assertEqual(len(random_string()), 5)
        self.assertEqual(len(random_string(10)), 10)
        self.assertEqual(len(random_string(10, upper_chars=False)), 10)
        self.assertEqual(len(random_string(10, punctuation=True)), 10)
        self.assertEqual(len(random_string(10, upper_chars=False,
                                           punctuation=True)), 10)
