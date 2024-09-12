#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import bouillon
from pathlib import Path


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == 'bouillon')


def test_run():
    bouillon.run(['ls'], )
    bouillon.run(['ls'], dry_run=True)
    bouillon.run(['unknown'], dry_run=True)


def test_check_for_test_files_fail(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    a = src / "a.py"
    a.write_text("a")
    b_foo =  src / "foo"
    b_foo.mkdir()
    b = b_foo / "b.py"
    b.write_text("b")

    test = tmp_path / "test"
    test.mkdir()
    test_a = test / "test_a.py"
    test_a.write_text("test_a")

    assert not bouillon.check_for_test_files(src, test)


def test_check_for_test_files(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    test = tmp_path / "test"
    test.mkdir()
    assert bouillon.check_for_test_files(src, test)

    a = src / "a.py"
    a.write_text("a")
    src_foo = src / "foo"
    src_foo.mkdir()
    b = src_foo / "b.py"
    b.write_text("b")

    test_a = test / "test_a.py"
    test_a.write_text("test_a")
    test_foo = test / "foo"
    test_foo.mkdir()
    test_b = test_foo / "test_b.py"
    test_b.write_text('test_b')

    assert bouillon.check_for_test_files(src, test)


def test_find_requirements():
    pass
