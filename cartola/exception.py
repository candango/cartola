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

import sys


class FauxTb(object):
    def __init__(self, tb_frame, tb_lineno, tb_next):
        self.tb_frame = tb_frame
        self.tb_lineno = tb_lineno
        self.tb_next = tb_next


def current_stack(skip=0):
    try:
        1/0
    except ZeroDivisionError:
        f = sys.exc_info()[2].tb_frame
    # On python 3 range works as xrange in python 2
    # See: https://stackoverflow.com/a/15014361/2887989
    for i in range(skip + 2):
        f = f.f_back
    lst = []
    while f is not None:
        lst.append((f, f.f_lineno))
        f = f.f_back
    return lst


def extend_traceback(tb, stack):
    """Extend traceback with stack info."""
    head = tb
    for tb_frame, tb_lineno in stack:
        head = FauxTb(tb_frame, tb_lineno, head)
    return head


def full_exc_info():
    """Like sys.exc_info, but includes the full traceback.

    See: https://stackoverflow.com/a/13210518/2887989

    Example:
    >>> import logging
    >>>
    >>> def func():
    >>>     try:
    >>>         raise Exception('Dummy')
    >>>     except:
    >>>         # Use full_exe_info with the logger exe_info parameter
    >>>         logging.error("Something awful happened!",
    >>>             exc_info=full_exc_info())
    >>>
    >>> def func2():
    >>>     func()
    >>>
    >>> func2()
    >>>
    """
    t, v, tb = sys.exc_info()
    full_tb = extend_traceback(tb, current_stack(1))
    return t, v, full_tb
