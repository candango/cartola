#!/usr/bin/env python
#
# Copyright 2015-2020 Flavio Garcia
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


# Variables to test config functions
my_string_value = "string"
my_num_value = 1
my_list_value = ["a", "list"]
my_dict_value = {'a': "dict"}


# Function to test config functions
def my_function():
    return my_string_value


# Class to test config functions
class MyClass:

    def __init__(self):
        self._num_value = my_num_value

    @property
    def num_value(self):
        return self._num_value
