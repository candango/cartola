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

"""
File system functions tests
"""

from __future__ import (absolute_import, division, print_function,
                        with_statement)

import tests
from cartola import fs
import os
import unittest


class FsExtensionTestCase(unittest.TestCase):

    def test_extension_file_with_extension(self):
        """ Happy scenario, a filename with an extension
        """
        filename = 'the_file.ext'
        expected_extension = 'ext'
        extension = fs.get_file_extension(filename)
        self.assertEqual(extension, expected_extension)
        self.assertTrue(fs.file_has_extension(filename))

    def test_extension_file_ending_with_dot(self):
        """ Filename ending with a dot
        """
        filename = 'the_file.'
        extension = fs.get_file_extension(filename)
        self.assertIsNone(extension)
        self.assertFalse(fs.file_has_extension(filename))

    def test_extension_file_no_extension(self):
        """ Filename without extension
        """
        filename = 'the_file'
        extension = fs.get_file_extension(filename)
        self.assertIsNone(extension)
        self.assertFalse(fs.file_has_extension(filename))


class FsModuleTestCase(unittest.TestCase):

    def tearDown(self):
        fs.remove_existing(tests.get_sandbox_path(
            os.path.join("monster", "__init__.py")))
        fs.remove_existing(tests.get_sandbox_path(
            os.path.join("monster", "of", "__init__.py")))
        fs.remove_existing(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "__init__.py")))
        fs.remove_existing(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "lake", "__init__.py")))
        fs.rmdir_existing(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "lake")))
        fs.rmdir_existing(tests.get_sandbox_path(
            os.path.join("monster", "of", "the")))
        fs.rmdir_existing(tests.get_sandbox_path(
            os.path.join("monster", "of")))
        fs.rmdir_existing(tests.get_sandbox_path(
            os.path.join("monster")))

    def test_fs_create_module(self):
        """ Create a module structure in a target directory. """
        fs.create_module("monster.of.the.lake", tests.SANDBOX_PATH)
        self.assertTrue(os.path.exists(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "lake")
        )))
        self.assertTrue(os.path.exists(tests.get_sandbox_path(
            os.path.join("monster", "__init__.py")
        )))
        self.assertTrue(os.path.exists(tests.get_sandbox_path(
            os.path.join("monster", "of", "__init__.py")
        )))
        self.assertTrue(os.path.exists(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "__init__.py")
        )))
        self.assertTrue(os.path.exists(tests.get_sandbox_path(
            os.path.join("monster", "of", "the", "lake", "__init__.py")
        )))


class FsBasicIOOperationsTestCase(unittest.TestCase):

    def setUp(self):
        """ Application configuration file will be read and components will be
        loaded.
        """
        self.file_to_read = "cartola_sandbox.txt"
        self.file_to_read_path = tests.get_sandbox_path(self.file_to_read)
        self.file_to_write = "cartola_file_write_test.txt"
        self.file_to_write_path = tests.get_sandbox_path(self.file_to_write)
        fs.remove_existing(self.file_to_write_path)

    def tearDown(self):
        fs.remove_existing(self.file_to_write_path)

    def test_string_fs_read(self):
        """ Read a file returning string as result. """
        expected = "Do not remove this file.\n"
        value = fs.read(self.file_to_read_path)
        self.assertIsInstance(value, str)
        self.assertEqual(expected, value)

    def test_binary_fs_read(self):
        """ Read a file returning bytes as result. """
        expected = b"Do not remove this file.\n"
        value = fs.read(self.file_to_read_path, True)
        self.assertIsInstance(value, bytes)
        self.assertEqual(expected, value)

    def test_string_fs_write(self):
        """ Write in a file using data as string. """
        data = "My text to write.\n"
        fs.write(self.file_to_write_path, data)
        self.assertTrue(os.path.exists(self.file_to_write_path))
        self.assertEqual(data, fs.read(self.file_to_write_path))

    def test_binary_fs_write(self):
        """ Write in a file using data as bytes. """
        data = b"My text to write.\n"
        fs.write(self.file_to_write_path, data, True)
        self.assertTrue(os.path.exists(self.file_to_write_path))
        self.assertEqual(data, fs.read(self.file_to_write_path, True))

    def test_fs_touch(self):
        """ Create(touch) a new file. """
        file_target = tests.get_sandbox_path("file_to_touch.txt")
        self.assertFalse(os.path.exists(file_target))
        fs.touch(file_target)
        self.assertTrue(os.path.exists(file_target))
        fs.remove_existing(file_target)

    def test_fs_remove_existing(self):
        """ Remove a file is it exists. """
        file_target = tests.get_sandbox_path("remove_existing_file.txt")
        self.assertFalse(fs.remove_existing(file_target))
        fs.touch(file_target)
        self.assertTrue(os.path.exists(file_target))
        self.assertTrue(fs.remove_existing(file_target))
        self.assertFalse(os.path.exists(file_target))

    def test_fs_rmdir_existing(self):
        """ Remove a directory is it exists. """
        dir_target = tests.get_sandbox_path("rmdir_existing_dir")
        self.assertFalse(fs.rmdir_existing(dir_target))
        os.mkdir(dir_target)
        self.assertTrue(os.path.exists(dir_target))
        self.assertTrue(fs.rmdir_existing(dir_target))
        self.assertFalse(os.path.exists(dir_target))
