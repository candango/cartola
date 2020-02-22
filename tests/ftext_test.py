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

"""
Formatted text functions tests
"""

from __future__ import (absolute_import, division, print_function,
                        with_statement)

from cartola import ftext
import unittest


class FtextTestCase(unittest.TestCase):

    def test_default_fstext_pad(self):
        """ Test default text pad """
        text = "my test"
        padded_text = ftext.pad(text)
        padded_text_x = padded_text[len(text):].split(" ")
        self.assertEqual(79, len(padded_text))
        self.assertEqual(79 + 1 - len(text), len(padded_text_x))
        for i in range(0, len(padded_text_x) - 1):
            self.assertEqual(padded_text_x[0], padded_text_x[i])

    def test_default_fstext_pad_center(self):
        """ Test default text pad centered """
        text = "my test"
        padded_text_center = ftext.pad(text, orientation="center")
        self.assertEqual(79, len(padded_text_center))
        self.assertEqual(padded_text_center[0],
                         padded_text_center[len(padded_text_center) - 1])
        # Centered from 0 to 36 and 43 and beyond
        self.assertEqual("", padded_text_center[0:36].replace(" ", ""))
        self.assertEqual("", padded_text_center[43:].replace(" ", ""))

    def test_default_fstext_pad(self):
        """ Test default text pad """
        text = "my test"
        padded_text = ftext.pad(text)
        padded_text_x = padded_text[len(text):].split(" ")
        self.assertEqual(79, len(padded_text))
        self.assertEqual(79 + 1 - len(text), len(padded_text_x))
        for i in range(0, len(padded_text_x) - 1):
            self.assertEqual(padded_text_x[0], padded_text_x[i])
