# -*- coding: UTF-8 -*-
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

import importlib
import yaml


def load_yaml_file(path):
    """ Returns the parsed structure from a yaml config file.

    :param path: Path where the yaml file is located.
    :return: The yaml configuration represented by the yaml file.
    """
    result = None
    with open(path, 'r') as steam:
        result = yaml.safe_load(steam)
    return result


def get_from_module(module, reference_name):
    """ Return a reference from a module and a class name parameters.
    The reference name must exists in the and could be a variable, a callable
    or a class.

    If reference name doesn't exists in the module it will return None.

    Example:
    >>> get_from_module("my.module", "my_object")
    >>> get_from_module("my.module", "my_function")
    >>> get_from_module("my.module", "MyClass")

    :param basestring module: The module name.
    :param basestring reference_name: What should be returned from the module.
    :return: The value resolved by the module and class name provided or None.
    """
    module = importlib.import_module(module)
    try:
        return getattr(module, reference_name)
    except AttributeError:
        return None


def get_from_string(full_reference):
    """ Return a reference from a string provided as a parameter.
    The reference name must have the an existing module with something to be
    returned from this module. This could be a variable, a callable or a class.

    Example:
    >>> get_from_string("my.module.my_object")
    >>> get_from_string("my.module.my_function")
    >>> get_from_string("my.module.Myclass")

    :param basestring full_reference: Absolute reference.
    :return: The reference resolved from the .
    """
    module = ".".join(full_reference.split(".")[:-1])
    reference = full_reference.split(".")[-1]
    if module.strip() != "":
        return get_from_module(module, reference)
    return None
