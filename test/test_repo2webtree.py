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

"""Basic tests running pkg.repo2webtree"""

import pathlib
import subprocess

srcdir = pathlib.Path(__file__).absolute().parent
data_dir = srcdir/'data'
top_srcdir = srcdir.parent

repo2webtree = top_srcdir/'pkg.repo2webtree'


def _dirs_equal(tmp_path, path_a, path_b):
    with open(tmp_path/'diff.stdout', 'x+') as diff_stdout, \
         open(tmp_path/'diff.stderr', 'x+') as diff_stderr:
        argv = ['gdiff', '-Nru', path_a, path_b]
        res = subprocess.run(argv, stdout=diff_stdout, stderr=diff_stderr)

        diff_stderr.seek(0)
        assert '' == diff_stderr.read()

        diff_stdout.seek(0)
        assert '' == diff_stdout.read()

        res.check_returncode()


def test_repo(tmp_path):
    got_dir = tmp_path/'webtree.got'
    exp_dir = data_dir/'webtree.expected'

    argv = [repo2webtree, data_dir/'example.repo', got_dir]
    subprocess.run(argv, check=True, timeout=5)

    _dirs_equal(tmp_path, exp_dir, got_dir)
