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

import calendar
from datetime import datetime


def extract_datetime(dictionary, key, mask):
    """ Extract a date time from a dictionary by it's key and if the value
    isn't a datetime will convert using a giving mask.

    :param dict dictionary:
    :param str|int key:
    :param str mask:
    :return: The date time from a dict by it's key
    :rtype: datetime
    """
    if dictionary.get(key) is None:
        return None
    if isinstance(dictionary.get(key), datetime):
        return dictionary.get(key)
    else:
        return datetime.strptime(dictionary.get(key), mask)


def last_day_of_month(year, month):
    """ Return the last day of a month. It is also necessary to provide a year.

    :param int year:
    :param int month:
    :return: The last day of month
    :rtype: int
    """
    return calendar.monthrange(year, month)[1]


def complete_month(year, month):
    """ Return a string with the month number padded with zero if the month has
    only one digit. It is also necessary to provide a year.

    :param year:
    :param month:
    :return: Month number padded with zero.
    :rtype: str
    """
    return datetime(year, month, 1).strftime("%m")
