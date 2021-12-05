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

from collections import namedtuple
import warnings


def first_row_in_page(page, per_page=10):
    return (int(page) * int(per_page)) + 1 - int(per_page)


class Paginator(object):
    """ Helps to manage generic pagination tasks.

    Internal parameters:

    Rows:
        _count: Row count. Must be provided
        _per_page: Rows per page to be used while handling pagination
    Pages:
        _page: Current page set in the paginator

    Blocks(of pages):
        _per_block: Pages per block of pages to be used while handling
        pagination
    """

    _count: int
    _page: int
    _per_page: int
    _per_block: int

    def __init__(self, count, **kwargs):
        self._count = count
        default_page = 1
        default_per_page = 10
        default_per_block = 10
        if "current_page" in kwargs:
            warnings.warn("The parameter 'current_page' is depreciated, use "
                          "'page' instead.", DeprecationWarning, 2)
            self._page = int(kwargs.get("current_page", default_page))
            # If page parameter isn't provided keep the value defined by the
            # depreciated parameter
            default_page = self._page
        self._page = int(kwargs.get("page", default_page))

        if "rows_per_page" in kwargs:
            warnings.warn("The parameter 'rows_per_page' is depreciated, use "
                          "'per_page' instead.", DeprecationWarning, 2)
            self._per_page = int(kwargs.get("rows_per_page", default_per_page))
            # If page parameter isn't provided keep the value defined by the
            # depreciated parameter
            default_per_page = self._per_page
        self._per_page = int(kwargs.get("per_page", default_per_page))

        if "pages_per_block" in kwargs:
            warnings.warn("The parameter 'pages_per_block' is depreciated, "
                          "use 'per_block' instead.", DeprecationWarning, 2)
            self._per_block = int(kwargs.get("pages_per_block",
                                  default_per_block))
            # If page parameter isn't provided keep the value defined by the
            # depreciated parameter
            default_per_block = self._per_block
        self._per_block = int(kwargs.get("per_block", default_per_block))

        # Fix current page if overflows the page count
        if self._page > self.pages:
            self._page = self.pages

    @property
    def row_count(self):
        warnings.warn("The property 'row_count' is depreciated, use 'count' "
                      "instead.", DeprecationWarning, 2)
        return self.count

    @property
    def count(self):
        return self._count

    @property
    def block_first_page(self):
        return self.first_page_in_block

    @property
    def first_page_in_block(self) -> int:
        # Returning the current fist page, in relation of the current block
        return (self.block * self._per_block) + 1 - self._per_block

    @property
    def block_last_page(self):
        warnings.warn("The property 'block_last_page' is depreciated, use "
                      "'last_page_in_block' instead.", DeprecationWarning, 2)
        return self.last_page_in_block

    @property
    def last_page_in_block(self) -> int:
        # Returning the current fist page, in relation of the current block
        # Setting current last page
        if self.is_last_block:
            return self.first_page_in_block + self.pages_last_block - 1
        return self.block * self._per_block

    @property
    def pages_last_block(self):
        # Returning the number of pages in the last block
        if self.pages < self._per_block:
            return self.pages
        else:
            return self._per_block if not (
                    self.pages % self._per_block) else (
                    self.pages % self._per_block)

    @property
    def is_first_page(self):
        return self._page == 1

    @property
    def is_last_page(self):
        return self._page == self.pages

    @property
    def is_last_block(self):
        return self.block == self.blocks

    @property
    def page_count(self):
        warnings.warn("The property 'page_count' is depreciated, use 'pages' "
                      "instead.", DeprecationWarning, 2)
        return self.pages

    @property
    def page(self):
        return self._page

    @property
    def pages(self):
        if self._count > 0:
            return int(self._count / self._per_page) + (
                1 if self._count % self._per_page else 0)
        return 0

    @property
    def current_block(self):
        warnings.warn("The property 'current_block' is depreciated, use "
                      "'block' instead.", DeprecationWarning, 2)
        return self.block

    @property
    def block(self):
        # Returning current block of pages
        if self._page <= self._per_block:
            return 1
        return int(self._page / self._per_block) + (
            1 if self._page % self._per_block else 0)

    @property
    def block_count(self):
        warnings.warn("The property 'block_count' is depreciated, use 'blocks'"
                      " instead.", DeprecationWarning, 2)
        return self.blocks

    @property
    def blocks(self):
        if self._count > 0:
            return int(self._count / self._per_page) + (
                1 if self._count % self._per_page else 0)

    @property
    def pages_in_block(self):
        # return the range of pages in the current block
        return range(self.first_page_in_block, self.last_page_in_block + 1)

    @property
    def current_first_row(self):
        warnings.warn("The property 'current_first_row' is depreciated, use "
                      "'first_row' instead.", DeprecationWarning, 2)
        return self.first_row

    @property
    def first_row(self) -> int:
        return self.first_row_in_page(self._page)

    @property
    def current_last_row(self):
        warnings.warn("The property 'current_last_row' is depreciated, use "
                      "'last_row' instead.", DeprecationWarning, 2)
        return self.last_row

    @property
    def last_row(self):
        # Return current last row
        if self.is_last_page:
            return self.first_row + self.rows_in_last_page - 1
        else:
            return self.page * self._per_page

    @property
    def rows_last_page(self):
        warnings.warn("The property 'rows_last_page' is depreciated, use "
                      "'rows_in_last_page' instead.", DeprecationWarning, 2)
        return self.rows_in_last_page

    @property
    def rows_in_last_page(self):
        # Setting rows in the last page
        return self._per_page if not (
                self._count % self._per_page) else (
                self._count % self._per_page)

    def offset(self, **kwargs):
        page = kwargs.get("page", self.page)
        if page > self.pages:
            message = ("Page %s is bigger than the number of pages %s." % (
                page, self.pages))
            raise IndexError(message)
        return self.first_row_in_page(page) - 1, self._per_page

    def offsets(self, **kwargs):
        page = kwargs.get("page", 1)
        return [self.offset(page=p) for p in range(page, self.pages+1)]

    def first_row_in_page(self, page):
        return first_row_in_page(page, self._per_page)


# TODO: Check if this is still necessary
PagedData = namedtuple('PagedData', ['data', 'count'])
