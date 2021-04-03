# -*- coding: UTF-8 -*-
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

import importlib
import yaml
import logging


def load_yaml_file(path):
    """ Returns the parsed structure from a yaml config file.

    :param path: Path where the yaml file is located.
    :return: The yaml configuration represented by the yaml file.
    """
    result = None
    with open(path, 'r') as steam:
        result = yaml.safe_load(steam)
    return result


def get_from_module(module, attr_name):
    """ Return a reference from a module.
    The attribute name must exist in the module, it could be a variable,
    a callable or a class.

    If reference name doesn't exists in the module it will return None.

    Example:
    >>> get_from_module("my.module", "my_object")
    >>> get_from_module("my.module", "my_function")
    >>> get_from_module("my.module", "MyClass")

    :param basestring module: The module name.
    :param basestring attr_name: What should be returned from the module.
    :return: The value resolved by the module and attr name provided or None.
    """
    module = importlib.import_module(module)
    try:
        return getattr(module, attr_name)
    except AttributeError:
        return None


def get_from_string(full_reference):
    """ Return a reference from a string provided as a parameter.
    The reference name must be resolved as a module and some attribute from
    this module, it could be a variable, a callable or a class.

    Example:
    >>> get_from_string("my.module.my_object")
    >>> get_from_string("my.module.my_function")
    >>> get_from_string("my.module.Myclass")

    :param basestring full_reference: Absolute reference.
    :return: The reference resolved from the .
    """
    module = ".".join(full_reference.split(".")[:-1])
    attr_name = full_reference.split(".")[-1]
    if module.strip() != "":
        return get_from_module(module, attr_name)
    return None


def get_from_dict(conf, **kwargs):
    """ Return an attribute from a configuration dict bit containing either
    a full reference for something defined in a module or a module and
    attribute to be returned.
    In case of only a reference by default index will be 'reference'.
    In case of module an attribute by default indixes are 'module' and 'attr'.
    It is possible to change those indexes using reference_index in case of
    a full reference or module and attr_index for the attribute.

    Examples:

    When the configuration has only reference information:
    >>> conf = {'reference': "my.module.MyClass"}
    >>> get_from_dict(conf)

    When the configuration has reference as 'module' and attribute index as
    'class':
    >>> conf = {'module': "my.module", 'my_class': "MyClass"}
    >>> get_from_dict(conf, attr_index="my_class")

    When the configuration has module index as 'amodule and attribute index as
    'my_class':
    >>> conf = {'amodule': "my.module", 'my_class': "MyClass"}
    >>> get_from_dict(conf, module_index="amodule",
    >>>     attr_index="my_class")

    :param dict conf: Configuration dict contained reference or/and attribute
    indexes.
    :key str reference_index: The index for the full
    :key str attr_index: Index to be used to get the class name
    :return: The class resolved at the module referred into the config.
    """
    reference_index = kwargs.get("reference_index", None)
    attr_index = kwargs.get("attr_index")
    if attr_index is None:
        if reference_index is None:
            reference_index = "reference"
        return get_from_string(conf[reference_index])
    # If attribute index is defined we're looking for module and attr by
    # default
    if reference_index is None:
        reference_index = "module"
    return get_from_module(conf[reference_index], conf[attr_index])


def log_level_from_string(str_level):
    """ Return the log level defined in the logging module by a sting.

    :param str_level: Log level string
    :return: The log level code
    """
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'WARN': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }
    try:
        return levels[str_level.upper()]
    except KeyError:
        pass
    except AttributeError:
        if str_level in [logging.DEBUG, logging.INFO, logging.WARNING,
                         logging.ERROR, logging.CRITICAL]:
            return str_level
    return logging.NOTSET
