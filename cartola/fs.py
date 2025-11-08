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

import os
import logging
from typing import Optional, List, Union
import warnings

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


def _append(path: str, data: Union[str, bytes], binary: bool = False):
    """
    Appends data to a file located in a given path.
    If binary is true will open the file with the binary flag.

    :param str path: Path where the file is located.
    :param str|bytes data: Data to be appended to the file.
    :param bool binary: If True, opens the file in binary append mode ('ab').
    """
    mode = "a"
    if binary:
        mode = "ab"
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes when appending in binary "
                            "mode.")
    else:
        if not isinstance(data, str):
            raise TypeError("Data must be a string when appending in text "
                            "mode.")

    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        with open(path, mode) as f:
            f.write(data)
    except Exception as e:
        print(f"ERROR: Failed to append to file '{path}' in mode '{mode}'. "
              f"Reason: {e}")


def b_append(path: str, data: bytes):
    """
    Appends data in binary mode ('ab') to a file located in a given path.

    :param str path: Path where the file is located.
    :param bytes data: Data to be written (must be bytes).
    """
    _append(path, data, True)


def s_append(path: str, data: str):
    """
    Appends data in string mode ('a') to a file located in a given path.

    :param str path: Path where the file is located.
    :param str data: Data to be written (must be string).
    """
    _append(path, data, False)


def b_write(path: str, data: bytes):
    """ Write data in binary mode to a file located in a given path.
    This is an alias to:

    >>> my_data = b"a data to be writen"
    >>> b_write("my_path", my_data)

    :param str path: Path where the file is located
    :param str|bytes data: Data to be writen in the file. If binary is true
    data must be in bytes instead of string.
    """
    _write(path, data, True)


def s_write(path: str, data: str):
    """ Write data in string mode to a file located in a given path.
    This is an alias to:

    >>> my_data = "a data to be writen"
    >>> s_write("my_path", my_data)

    :param str path: Path where the file is located
    :param str|bytes data: Data to be writen in the file. If binary is true
    data must be in bytes instead of string.
    """
    _write(path, data)


def _write(path: str, data, binary: bool = False):
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


def write(path: str, data, binary: bool = False):
    """ Write data to a file located in a given path. If binary is true will
    open the file with the binary flag and data should be bytes instead of
    string.
    :param str path: Path where the file is located
    :param str|bytes data: Data to be writen in the file. If binary is true
    data must be in bytes instead of string.
    :param bool binary: If true will read the file with the binary flag
    """
    warnings.warn("The function 'write' is depreciated, use either 'b_write' "
                  "or s_write.", DeprecationWarning, 2)
    _write(path, data, binary)


def _read_and_slice(path: str, mode: str = "r", offset: Optional[int] = None,
                    start_line: Optional[int] = None,
                    limit: Optional[int] = None
                    ) -> List[str]:
    """
    Reads a file line-by-line and returns a list of lines, sliced
    according to the offset, start_line, and limit parameters.

    :param str path: Path where the file is located.
    :param str mode: Mode to be used file opening the file, r is the default
    mode value.
    :param Optional[int] offset: Number of lines for head/tail if
    start_line/limit are None.
        - Positive integer (e.g., 10): Return the first 10 lines (head).
        - Negative integer (e.g., -10): Return the last 10 lines (tail).
    :param Optional[int] start_line: 1-based index of the line to start reading
    from.
    :param Optional[int] limit: The maximum number of lines to read starting
    from start_line.
    :return List[str]: A list of the requested lines.
    """
    abs_path = os.path.abspath(path)
    try:
        with open(abs_path, mode) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"ERROR: Failed to read file '{path}'. Reason: {e}")
        return []

    #  Handle Start Line and Limit
    if start_line is not None and limit is not None:
        # Convert 1-based index to 0-based index
        start_index = max(0, start_line - 1)
        end_index = start_index + limit

        return lines[start_index:end_index]

    # Handle Offset (Head/Tail, fallback if start_line/limit not used)
    elif offset is not None and offset != 0:
        if offset > 0:
            # Head: return the first 'offset' lines
            return lines[:offset]
        else:
            # Tail: return the last 'offset' lines (negative indexing in
            # Python)
            return lines[offset:]

    return lines


def read(path: str, binary: bool = False, offset: Optional[int] = None,
         start_line: Optional[int] = None, limit: Optional[int] = None
         ) -> Union[str, bytes]:
    """
    Read a file located at the given path. Supports reading a specific number
    of lines from the start (head/tail via offset) or a specific line range
    (via start_line and limit).

    :param str path: Path where the file is located.
    :param bool binary: If true will read the file with the binary flag.
    :param Optional[int] offset: Number of lines to return (for head/tail).
    :param Optional[int] start_line: 1-based index of the line to start reading
    from.
    :param Optional[int] limit: The maximum number of lines to read starting
    from start_line.
    :return str|bytes: File content (string or bytes).
    """
    abs_path = path
    if not os.path.isabs(abs_path):
        abs_path = os.path.join(os.getcwd(), abs_path)

    mode = "r"
    joiner = ""
    if binary:
        mode = "rb"
        joiner = b""

    lines = _read_and_slice(path, mode, offset, start_line, limit)
    return joiner.join(lines)


def touch(path):
    """ Creates a file located at the given path. """
    with open(path, 'a') as _:
        os.utime(path, None)


def remove_existing(file_path):
    """ Remove a file in a path if it exists and returns true. If the file
    doesn't exist returns false.

    :param file_path: The file path
    :return bool: True if file exits
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def rmdir_existing(dir_path):
    """ Remove a directory in a path if it exists and returns true. If
    directory doesn't exist returns false.

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
