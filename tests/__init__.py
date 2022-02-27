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

import logging
import os
import warnings

# Setting root path
ROOT = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(ROOT, "fixtures")
SANDBOX_PATH = os.path.join(ROOT, "sandbox")


def get_fixture_path(path):
    return os.path.join(FIXTURES_PATH, path)


def get_sandbox_path(path):
    return os.path.join(SANDBOX_PATH, path)


def safe_remove(path):
    if os.path.exists(path):
        os.remove(path)


def safe_rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)


class WarningsHandler(logging.Handler):
    def handle(self, record):
        if record.levelno == logging.WARN:
            warnings.warn(record.getMessage())
        return record
