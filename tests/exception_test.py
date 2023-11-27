# -*- coding: UTF-8 -*-
#
# Copyright 2015-2023 Flavio Garcia
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

from tests import WarningsHandler
from cartola import exception
import logging
import warnings
import unittest

logger = logging.getLogger(__name__)


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).

    See: https://stackoverflow.com/a/20553331/2887989
    """

    def __init__(self, *args, **kwargs):
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
                         'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        """Store a message from ``record`` in the instance's ``messages``
        dict."""
        try:
            self.messages[record.levelname.lower()].append(record)
        except Exception:
            self.handleError(record)

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()


class ExceptionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ExceptionTestCase, cls).setUpClass()
        # Assuming you follow Python's logging module's documentation's
        # recommendation about naming your module's logs after the module's
        # __name__,the following getLogger call should fetch the same logger
        # you use in the foo module
        exception_log = logging.getLogger(__name__)
        cls._exception_log_handler = MockLoggingHandler(level='DEBUG')
        exception_log.addHandler(cls._exception_log_handler)
        cls.exception_log_messages = cls._exception_log_handler.messages

    def setUp(self):
        super(ExceptionTestCase, self).setUp()
        self._exception_log_handler.reset()  # So each test is independent

    def test_stack(self):
        """ Checking if full_exc_info will return the division by 0 error at
        line 83. If the line changes this test will fail."""
        try:
            1/0
        except ZeroDivisionError:
            logger.warning("The message", exc_info=exception.full_exc_info())
            for record in self.exception_log_messages['warning']:
                tb_frame = record.exc_info[2]
                while tb_frame.tb_next:
                    tb_frame = tb_frame.tb_next
                self.assertEqual(
                    tb_frame.tb_frame.f_locals['record'].filename,
                    "exception_test.py")
                self.assertEqual(
                    tb_frame.tb_frame.f_locals['record'].funcName,
                    "test_stack")
                self.assertEqual(
                    tb_frame.tb_frame.f_locals['record'].exc_info[0],
                    ZeroDivisionError)
                self.assertEqual(tb_frame.tb_lineno, 83)
