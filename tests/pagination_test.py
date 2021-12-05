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
Pagination tests
"""

from cartola import pagination
import logging
import warnings
import unittest


class WarningsHandler(logging.Handler):
    def handle(self, record):
        if record.levelno == logging.WARN:
            warnings.warn(record.getMessage())
        return record


class PaginatorTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.handler = WarningsHandler()
        #self.logger.addHandler(WarningsHandler())
        warnings.simplefilter("always")

    def tearDown(self):
        self.logger.removeHandler(self.handler)

    def test_paginator_depreciation(self):
        """ Test paginator depreciation methods and parameters """
        with warnings.catch_warnings(record=True) as w:
            paginator = pagination.Paginator(9, current_page=1,
                                             rows_per_page=10)

            warning = w.pop()
            self.assertEqual("The parameter 'rows_per_page' is depreciated, "
                             "use 'per_page' instead.",
                             warning.message.args[0])
            warning = w.pop()
            self.assertEqual("The parameter 'current_page' is depreciated, "
                             "use 'page' instead.", warning.message.args[0])
            self.assertEqual(1, paginator.page_count)
            warning = w.pop()
            self.assertEqual("The property 'page_count' is depreciated, use "
                             "'pages' instead.", warning.message.args[0])
            self.assertEqual(1, paginator.pages)
            self.assertEqual(9, paginator.row_count)
            warning = w.pop()
            self.assertEqual("The property 'row_count' is depreciated, use "
                             "'count' instead.", warning.message.args[0])
            self.assertEqual(1, paginator.current_first_row)
            warning = w.pop()
            self.assertEqual("The property 'current_first_row' is depreciated,"
                             " use 'first_row' instead.",
                             warning.message.args[0])
            self.assertEqual(9, paginator.current_last_row)
            warning = w.pop()
            self.assertEqual("The property 'current_last_row' is depreciated,"
                             " use 'last_row' instead.",
                             warning.message.args[0])

    def test_paginator_one_page(self):
        """ Test paginator with one page """
        paginator = pagination.Paginator(7, page=2)
        self.assertEqual(1, paginator.pages)
        self.assertEqual(7, paginator.count)
        self.assertEqual(1, paginator.first_row)
        self.assertEqual(7, paginator.last_row)

    def test_paginator_in_the_middle(self):
        """ Test paginator with one page """
        paginator = pagination.Paginator(64, page=5, per_page=6)
        self.assertEqual(5, paginator.page)
        self.assertEqual(11, paginator.pages)
        self.assertEqual(64, paginator.count)
        self.assertEqual(4, paginator.rows_in_last_page)
        self.assertEqual(25, paginator.first_row)
        self.assertEqual(30, paginator.last_row)

    def test_paginator_rows_last_page_less_than_per_page(self):
        """ Test paginator with one page """
        paginator = pagination.Paginator(93, page=15, per_page=7)
        self.assertEqual(14, paginator.page)
        self.assertEqual(14, paginator.pages)
        self.assertEqual(93, paginator.count)
        self.assertEqual(2, paginator.rows_in_last_page)
        self.assertEqual(92, paginator.first_row)
        self.assertEqual(93, paginator.last_row)

    def test_paginator_rows_last_page_equal_per_page(self):
        """ Test paginator with one page """
        paginator = pagination.Paginator(30, page=3)
        self.assertEqual(3, paginator.pages)
        self.assertEqual(3, paginator.page)
        self.assertEqual(30, paginator.count)
        self.assertEqual(21, paginator.first_row)
        self.assertEqual(30, paginator.last_row)

    def test_offset(self):
        """ Test the offset method to be used directly with a database query
        implementation """
        paginator = pagination.Paginator(1000)
        self.assertEqual((0, 10), paginator.offset())
        self.assertEqual((40, 10), paginator.offset(page=5))
        print(paginator.pages)
        try:
            self.assertEqual((100, 10), paginator.offset(page=101))
        except IndexError as ie:
            message = "Page 101 is bigger than the number of pages 100."
            self.assertEqual(ie.args[0], message)

    def test_offsets(self):
        """ Test the offset generator too loop through all offsets existent
        from page 1 to last page """
        paginator = pagination.Paginator(1000)
        self.assertEqual(100, len(paginator.offsets()))
        self.assertEqual(86, len(paginator.offsets(page=15)))
        self.assertEqual((590, 10), paginator.offsets(page=60)[0])
