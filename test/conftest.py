# SPDX-License-Identifier: 0BSD
#
# Copyright (c) 2022 Sine Nomine Associates.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import pytest

# Configure pytest so tests marked with @pytest.mark.destructive are skipped by
# default. If someone runs pytest with the --destructive arg, then the marked
# tests are not skipped.


def pytest_addoption(parser):
    parser.addoption("--destructive", action='store_true', default=False,
                     help="run destructive tests")


def pytest_configure(config):
    config.addinivalue_line('markers', "destructive: mark test as destructive")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--destructive"):
        # do not skip destructive tests
        return
    skip_mark = pytest.mark.skip(reason="option --destructive not given")
    for item in items:
        if 'destructive' in item.keywords:
            item.add_marker(skip_mark)
