# -*- coding: UTF-8 -*-
#
# Copyright 2015-2022 Flavio Garcia
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
if os.name == 'posix':
    import crypt
from hmac import compare_digest as compare_hash
import logging
import string

logger = logging.getLogger(__name__)


# Used implementations described on: http://bit.ly/2gHlH9z
# Recommended here: http://bit.ly/2fm97H3
# Confirmed here:
# https://docs.python.org/2/library/random.html#random.SystemRandom
def random_string(length=5, upper_chars=True, punctuation=False):
    """
    Generate a random string with the size equal to the given length.

    The string is based on random choices from a sequence of ascii lower case
    characters and digits.

    If length is not informed the string size will be 5.
    """
    chars = string.ascii_lowercase + string.digits
    if upper_chars:
        chars += string.ascii_uppercase
    if punctuation:
        chars += string.punctuation
    import secrets
    return ''.join(secrets.choice(chars) for _ in range(length))


# Key manager functionality is available only for posix.
# TODO: Figure out how to get this working on nt(windows).
if os.name == 'posix':
    class KeyManager(object):
        # following: https://crackstation.net/hashing-security.htm
        if (sys.version_info.major, sys.version_info.minor) > (3, 6):
            METHOD_BLOWFISH = crypt.METHOD_BLOWFISH
        METHOD_MD5 = crypt.METHOD_MD5
        METHOD_CRYPT = crypt.METHOD_CRYPT
        METHOD_SHA512 = crypt.METHOD_SHA512
        METHOD_SHA256 = crypt.METHOD_SHA256

        @staticmethod
        def get_manager(method):
            """ Return a key manager by it's key method.

            :param method:
            :return: A key manger by it's key method
            :rtype: KeyManager
            """
            managers = {
                KeyManager.METHOD_CRYPT: CryptKeyManager,
                KeyManager.METHOD_MD5: Md5Manager,
                KeyManager.METHOD_SHA512: Sha512KeyManager,
                KeyManager.METHOD_SHA256: Sha256KeyManager,
            }
            if (sys.version_info.major, sys.version_info.minor) >= (3, 7):
                managers[KeyManager.METHOD_BLOWFISH] = BlowfishKeyManager
            manager = managers.get(method, NotImplemented)
            return manager()

        def generate(self, secret, **kwargs):
            """ Generate a hash using crypt the method will be chosen from the
            salt implemented or provided. If salt isn't provided a salt will be
            generated during the processing, it is necessary to extract the
            salt from the returned hash in order to validate it again.

            :param str secret:
            :param dict kwargs:
            :key salt:
            :key pepper:
            :return:
            :rtype: str
            """
            salt = kwargs.get("salt", self.salt(**kwargs))
            pepper = kwargs.get("pepper")
            if pepper:
                secret = "%s%s" % (secret, pepper)
            return crypt.crypt(secret, salt)

        @staticmethod
        def salt_from_hash(_hash):
            return "$".join(_hash.split("$")[:-1])

        def salt(self, **kwargs):
            raise NotImplementedError

        def _salt_it(self, method, **kwargs):
            rounds = kwargs.get("rounds")
            if (sys.version_info.major, sys.version_info.minor) > (3, 6):
                salt = crypt.mksalt(method=method, rounds=rounds)
            else:
                salt = crypt.mksalt(method=method)
            return salt

        def validate(self, secret, _hash, **kwargs):
            salt = kwargs.get("salt", self.salt_from_hash(_hash))
            kwargs['salt'] = salt
            return compare_hash(self.generate(secret, **kwargs), _hash)


    class BlowfishKeyManager(KeyManager):

        def salt(self, **kwargs):
            return self._salt_it(crypt.METHOD_BLOWFISH, **kwargs)


    class CryptKeyManager(KeyManager):

        def salt(self, **kwargs):
            return self._salt_it(crypt.METHOD_CRYPT, **kwargs)


    class Md5Manager(KeyManager):

        def salt(self, **kwargs):
            return self._salt_it(crypt.METHOD_MD5, **kwargs)


    class Sha512KeyManager(KeyManager):

        def salt(self, **kwargs):
            return self._salt_it(crypt.METHOD_SHA512, **kwargs)


    class Sha256KeyManager(KeyManager):

        def salt(self, **kwargs):
            return self._salt_it(crypt.METHOD_SHA256, **kwargs)
