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

"""Tests for running 'pkg' commands against a local webserver."""

import contextlib
import functools
import http.server
import os
import pathlib
import pytest
import subprocess
import threading

HOST = 'localhost'
PORT = 9001
URL = f'http://{HOST}:{PORT}'

srcdir = pathlib.Path(__file__).absolute().parent
data_dir = srcdir/'data'
top_srcdir = srcdir.parent

repo2webtree = top_srcdir/'pkg.repo2webtree'


class _Webserver(threading.Thread):
    httpd = None

    def __init__(self, webroot):
        self.started = threading.Event()
        self.webroot = webroot
        super().__init__()

    def run(self):
        handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                    directory=self.webroot)

        with http.server.ThreadingHTTPServer((HOST, PORT), handler) as httpd:
            self.httpd = httpd
            self.started.set()
            httpd.serve_forever()


@pytest.fixture
def web_root(tmp_path):
    return tmp_path/'web_root'


@pytest.fixture
def webserver(web_root):
    server = _Webserver(web_root)
    server.start()
    assert server.started.wait(timeout=5)

    try:
        yield
    finally:
        server.httpd.shutdown()


def _run(argv, check=True):
    arg_str = ' '.join(str(arg) for arg in argv)
    print(f"+ {arg_str}")
    subprocess.run(argv, check=check, timeout=30)


def test_pkgrepo_info(web_root, webserver):
    _run([repo2webtree, data_dir/'example.repo', web_root])
    _run(['pkgrepo', 'info', '-s', URL])


@pytest.mark.destructive
def test_pkg_install(web_root, webserver):
    _run([repo2webtree, data_dir/'example.repo', web_root])

    try:
        _run(['pkg', 'set-publisher', '-g', URL, 'example.com'])
        try:
            _run(['pkg', 'install', 'example'])
            with open('/usr/bin/foo') as fh:
                assert fh.read() == '#!/bin/sh\necho foo\n'

        finally:
            _run(['pkg', 'uninstall', 'example'])
    finally:
        _run(['pkg', 'unset-publisher', 'example.com'])
