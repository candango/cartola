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
Security tests
"""

from cartola.security import random_string
import unittest


class RandomStringTestCase(unittest.TestCase):

    def test_random_string(self):
        """ Random string generation """
        self.assertNotEqual(random_string(), None)
        self.assertEqual(len(random_string()), 5)
        self.assertEqual(len(random_string(10)), 10)
        self.assertEqual(len(random_string(10, upper_chars=False)), 10)
        self.assertEqual(len(random_string(10, punctuation=True)), 10)
        self.assertEqual(len(random_string(10, upper_chars=False,
                                           punctuation=True)), 10)

    def test_sha512_without_pepper(self):
        """ Manager generation and verification on SHA512 without pepper"""
        key_manager = KeyManager.get_manager(KeyManager.METHOD_SHA512)
        hash_result = key_manager.generate(self.password)
        salt = key_manager.salt_from_hash(hash_result)
        self.assertTrue(hash_result.startswith(salt))
        self.assertTrue(key_manager.validate(self.password, hash_result))
        self.assertFalse(key_manager.validate(self.bad_password, hash_result))

    def test_sha512_with_pepper(self):
        """ Manager generation and verification on SHA512 and pepper"""
        key_manager = KeyManager.get_manager(KeyManager.METHOD_SHA512)
        hash_result = key_manager.generate(self.password, pepper=self.pepper)
        salt = key_manager.salt_from_hash(hash_result)
        self.assertTrue(hash_result.startswith(salt))
        self.assertTrue(key_manager.validate(self.password, hash_result,
                                             pepper=self.pepper))
        self.assertFalse(key_manager.validate(self.password, hash_result))
        self.assertFalse(key_manager.validate(self.bad_password, hash_result,
                                              pepper=self.pepper))

    def test_sha256_without_pepper(self):
        """ Manager generation and verification on SHA256 without pepper"""
        key_manager = KeyManager.get_manager(KeyManager.METHOD_SHA256)
        hash_result = key_manager.generate(self.password)
        salt = key_manager.salt_from_hash(hash_result)
        self.assertTrue(hash_result.startswith(salt))
        self.assertTrue(key_manager.validate(self.password, hash_result))
        self.assertFalse(key_manager.validate(self.bad_password, hash_result))

    def test_sha256_with_pepper(self):
        """ Manager generation and verification on SHA256 and pepper"""
        key_manager = KeyManager.get_manager(KeyManager.METHOD_SHA256)
        hash_result = key_manager.generate(self.password, pepper=self.pepper)
        salt = key_manager.salt_from_hash(hash_result)
        self.assertTrue(hash_result.startswith(salt))
        self.assertTrue(key_manager.validate(self.password, hash_result,
                                             pepper=self.pepper))
        self.assertFalse(key_manager.validate(self.password, hash_result))
        self.assertFalse(key_manager.validate(self.bad_password, hash_result,
                                              pepper=self.pepper))
