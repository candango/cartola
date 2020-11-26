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

import os
import logging
logger = logging.getLogger(__name__)


def create_module(module, target):
    """ Create a module directory structure into the target directory. """
    module_x = module.split('.')
    cur_path = ''
    for path in module_x:
        cur_path = os.path.join(cur_path, path)
        if not os.path.isdir(os.path.join(target, cur_path)):
            os.mkdir(os.path.join(target, cur_path))
        if not os.path.exists(os.path.join(target, cur_path, '__init__.py')):
            touch(os.path.join(target, cur_path, '__init__.py'))
    return cur_path


def file_has_extension(filename):
    """ Return True if the informed filename was extension on it.

    :param filename: The filename.
    :return: True if has extension.
    """
    if get_file_extension(filename) is None:
        return False
    return True


def get_file_extension(filename):
    """ Return the extension if the filename has it. None if not.

    :param filename: The filename.
    :return: Extension or None.
    """
    filename_x = filename.split('.')
    if len(filename_x) > 1:
        if filename_x[-1].strip() != "":
            return filename_x[-1]
    return None


def write(path, data, binary=False):
    """ Write data to a file located in a given path. If binary is true will
    open the file with the binary flag and data should be bytes instead of
    string.
    :param str path: Path where the file is located
    :param str|bytes data: Data to be writen in the file. If binary is true
    data must be in bytes instead of string.
    :param bool binary: If true will read the file with the binary flag
    """
    mode = "w"
    if binary:
        mode = "wb"
    with open(path, mode) as f:
        f.write(data)


def read(path, binary=False):
    """
    Read a file located at the given path. If binary is true will return bytes
    instead of string.

    :param str path: Path where the file is located
    :param bool binary: If true will read the file with the binary flag
    :return str|bytes: File content string or bytes. """
    data = None
    mode = "r"
    if binary:
        mode = "rb"
    abs_path = path
    if not os.path.isabs(abs_path):
        abs_path = os.path.join(os.getcwd(), abs_path)
    with open(abs_path, mode) as f:
        data = f.read()
    return data


def touch(path):
    """ Creates a file located at the given path. """
    with open(path, 'a') as f:
        os.utime(path, None)


def remove_existing(file_path):
    """ Remove a file in a path if it exists and returns true. If file doesn't
    exists returns false.

    :param file_path: The file path
    :return bool: True if file exits
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def rmdir_existing(dir_path):
    """ Remove a directory in a path if it exists and returns true. If
    directory doesn't exists returns false.

    :param dir_path: The directory path
    :return bool: True if directory exits
    """
    if os.path.exists(dir_path):
        os.rmdir(dir_path)
        return True
    return False


def only_dirs_from(path, absolute=True):
    """ Return only the directories into the informed path. By default the
    directory list will contain absolute paths.
    If path isn't a file will return None and log a warning.

    :param str path: The path to return files from
    :param bool absolute: If we return the just directory name or absolute path
    :return list or None: List of directories into the path
    """
    if os.path.isdir(path):
        return [os.path.join(path, item) if absolute else item
                for item in os.listdir(path)
                if os.path.isdir(os.path.join(path, item))]
    logger.warning("The informed path %s isn't a directory." % path)
    return None


def only_files_from(path, absolute=True, link=False):
    """ Return only files found into the informed path. By default the
    file list will contain absolute paths.
    If path isn't a file will return None and log a warning.

    :param str path: The path to return directories from
    :param bool absolute: If we return the just file name or absolute path
    :param bool link: If links should be returned also
    :return list or None: List of files into the path
    """
    def is_file_fs(fs_path, fs_link=False):
        if fs_link:
            return os.path.isfile(fs_path) or os.path.islink(fs_path)
        return os.path.isfile(fs_path)
    if os.path.isdir(path):
        return [os.path.join(path, item) if absolute else item
                for item in os.listdir(path)
                if is_file_fs(os.path.join(path, item), link)]
    logger.warning("The informed path %s isn't a directory." % path)
    return None
