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
Config functions tests
"""

from tests import get_fixture_path
from tests import fixtures
from cartola import config
import unittest
import logging


class ConfigGetFromTestCase(unittest.TestCase):

    def test_get_from_module(self):
        """ Test values returned by the get_from_string
        """
        self.assertEqual(None, config.get_from_module(
            "tests.fixtures", "my_string_value1"))
        self.assertEqual(fixtures.my_string_value, config.get_from_module(
            "tests.fixtures", "my_string_value"))
        self.assertEqual(fixtures.my_num_value, config.get_from_module(
            "tests.fixtures", "my_num_value"))
        self.assertEqual(fixtures.my_list_value, config.get_from_module(
            "tests.fixtures", "my_list_value"))
        self.assertEqual(fixtures.my_dict_value, config.get_from_module(
            "tests.fixtures", "my_dict_value"))
        my_function = config.get_from_module("tests.fixtures", "my_function")
        self.assertEqual(fixtures.my_function, my_function)
        self.assertEqual(fixtures.my_string_value, my_function())
        my_class = config.get_from_module("tests.fixtures", "MyClass")
        an_object = my_class()
        self.assertEqual(fixtures.MyClass, my_class)
        self.assertEqual(fixtures.my_num_value, an_object.num_value)

    def test_get_from_string(self):
        """ Test values returned by the get_from_string
        """
        self.assertEqual(None, config.get_from_string(
            "tests"))
        self.assertEqual(fixtures.my_string_value, config.get_from_string(
            "tests.fixtures.my_string_value"))
        self.assertEqual(fixtures.my_num_value, config.get_from_string(
            "tests.fixtures.my_num_value"))
        self.assertEqual(fixtures.my_list_value, config.get_from_string(
            "tests.fixtures.my_list_value"))
        self.assertEqual(fixtures.my_dict_value, config.get_from_string(
            "tests.fixtures.my_dict_value"))
        my_function = config.get_from_string("tests.fixtures.my_function")
        self.assertEqual(fixtures.my_function, my_function)
        self.assertEqual(fixtures.my_string_value, my_function())
        my_class = config.get_from_string("tests.fixtures.MyClass")
        an_object = my_class()
        self.assertEqual(fixtures.MyClass, my_class)
        self.assertEqual(fixtures.my_num_value, an_object.num_value)

    def test_get_from_dict(self):
        """ Test values returned by the get_from_dict
        """
        self.assertEqual(None, config.get_from_dict(
            {'reference': "my_string_value1"}))
        self.assertEqual(fixtures.my_string_value, config.get_from_dict(
            {'reference': "tests.fixtures.my_string_value"}))
        self.assertEqual(fixtures.my_num_value, config.get_from_dict(
            {'module': "tests.fixtures", 'attr': "my_num_value"},
            attr_index="attr"))
        self.assertEqual(fixtures.my_list_value, config.get_from_dict(
            {'module': "tests.fixtures", 'list': "my_list_value"},
            attr_index="list"))
        self.assertEqual(fixtures.my_dict_value, config.get_from_dict(
            {'module': "tests.fixtures", 'dict': "my_dict_value"},
            attr_index="dict"))
        my_function = config.get_from_dict(
            {'amodule': "tests.fixtures", 'function': "my_function"},
            reference_index="amodule", attr_index="function")
        self.assertEqual(fixtures.my_function, my_function)
        self.assertEqual(fixtures.my_string_value, my_function())
        my_class = config.get_from_dict(
            {'module': "tests.fixtures", 'class': "MyClass"},
            attr_index="class")
        an_object = my_class()
        self.assertEqual(fixtures.MyClass, my_class)
        self.assertEqual(fixtures.my_num_value, an_object.num_value)


class ConfigLoadYamlTestCase(unittest.TestCase):

    def test_load_yaml_file(self):
        a_file_path = get_fixture_path("a_file.yml")
        a_config = config.load_yaml_file(a_file_path)
        self.assertEqual(a_config['a']['item'], "a value")


class LogLevelTestCase(unittest.TestCase):

    def test_log_level_from_string(self):
        self.assertEqual(logging.WARNING,
                         config.log_level_from_string("WARNING"))
        self.assertEqual(logging.WARNING,
                         config.log_level_from_string("WARN"))
        self.assertEqual(logging.INFO,
                         config.log_level_from_string("INFO"))
        self.assertEqual(logging.ERROR,
                         config.log_level_from_string("ERROR"))
        self.assertEqual(logging.DEBUG,
                         config.log_level_from_string("DEBUG"))
        self.assertEqual(logging.CRITICAL,
                         config.log_level_from_string("CRITICAL"))
        self.assertEqual(logging.NOTSET,
                         config.log_level_from_string("NOTSET"))
