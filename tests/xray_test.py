# -*- coding: UTF-8 -*-
#
# Copyright 2015-2022 Flávio Gonçalves Garcia
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

from cartola import xray
import functools
import unittest
import sys


def decorator1(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(self, *args, **kwargs)
    return wrapper


@decorator1
class MyClass:

    @property
    def a_property(self):
        return "a property value"

    @decorator1
    def test(self):
        pass


class XrayTestCase(unittest.TestCase):

    def test_class_decorators(self):
        """ Test if the method class_decorators will return decorators
        properly."""
        # Testing passing a class as target
        decorators = xray.class_decorators(MyClass)
        self.assertTrue("MyClass" in decorators)
        self.assertTrue(decorators['MyClass'][0], "decorator1")

        # Testing passing a module as target
        decorators = xray.class_decorators(sys.modules[__name__])
        self.assertTrue("MyClass" in decorators)
        self.assertEqual(decorators['MyClass'][0], "decorator1")
        self.assertTrue("XrayTestCase" in decorators)
        self.assertEqual(len(decorators['XrayTestCase']), 0)

    def test_methods_decorators(self):
        """ Test if the get_method_decorators will return decorators
        properly."""
        decorators = xray.methods_decorators(MyClass)
        self.assertTrue("a_property" in decorators)
        self.assertEqual(decorators['a_property'][0], "property")
        self.assertTrue("test" in decorators)
        self.assertEqual(decorators['test'][0], "decorator1")
