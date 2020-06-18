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

from collections import namedtuple


def page_first_row(page, rows_per_page=10):
    return (int(page) * int(rows_per_page)) + 1 - int(rows_per_page)


class Paginator(object):

    def __init__(self, row_count, current_page=None, rows_per_page=10,
                 pages_per_block=10):
        if current_page is None or current_page == 0:
            current_page = 1

        self.row_count = row_count
        self.rows_per_page = rows_per_page

        self.current_page = int(current_page)

        self.block_count = 0
        self.current_block = 0
        self.pages_per_block = pages_per_block
        self.pages_last_block = 0

        self.block_first_page = 0
        self.block_last_page = 0

        # Fixed current if overflows the row count
        if self.page_count < self.current_page:
            self.current_page = self.page_count

        # Setting block count
        self.block_count = int(self.page_count / self.pages_per_block) + (
            1 if self.page_count % self.pages_per_block else 0)

        # Setting pages in the last block of pages
        if self.page_count < self.pages_per_block:
            self.pages_last_block = self.page_count
        else:
            self.pages_last_block = self.pages_per_block if not(
                self.page_count % self.pages_per_block) else (
                self.page_count % self.pages_per_block)

        # Setting current block of pages
        if self.current_page <= self.pages_per_block:
            self.current_block = 1
        else:
            self.current_block = int(
                self.current_page / self.pages_per_block) + (
                1 if self.current_page % self.pages_per_block else 0)

        # Setting current first page
        self.block_first_page = ((self.current_block * self.pages_per_block
                                    ) + 1 - self.pages_per_block)
        # Setting current last page
        if self.current_block == self.block_count:
            self.block_last_page = (self.block_first_page +
                                    self.pages_last_block - 1)
        else:
            self.block_last_page = (self.current_block *
                                    self.pages_per_block)

    @property
    def is_first_page(self):
        if self.current_page == 1:
            return True
        return False

    @property
    def is_last_page(self):
        if self.current_page == self.page_count:
            return True
        return False

    @property
    def page_count(self):
        if self.row_count > 0:
            return int(self.row_count / self.rows_per_page) + (
                1 if self.row_count % self.rows_per_page else 0)

    @property
    def block_pages(self):
        return range(self.block_first_page, self.block_last_page+1)

    @property
    def current_first_row(self):
        return self.page_first_row(self.current_page)

    @property
    def current_last_row(self):
        # Setting current last row
        if self.current_page == self.page_count:
            return self.current_first_row + self.rows_last_page - 1
        else:
            return self.current_page * self.rows_per_page

    @property
    def rows_last_page(self):
        # Setting rows in the last page
        return self.rows_per_page if not (
                self.row_count % self.rows_per_page) else (
                self.row_count % self.rows_per_page)

    def page_first_row(self, page):
        return (
            (int(page) * int(self.rows_per_page)) + 1 - int(self.rows_per_page)
        )


PagedData = namedtuple('PagedData', ['data', 'count'])
