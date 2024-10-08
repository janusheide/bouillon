# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import bouillon


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == "bouillon")


def test_run():
    bouillon.run(["ls"] )
    bouillon.run(["ls"], dry_run=True)
    bouillon.run(["unknown"], dry_run=True)


def test_check_for_test_files_fail(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    a = src / "a.py"
    a.write_text("a")

    foo = src / "foo"
    foo.mkdir()
    b = foo / "b.py"
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
    foo = src / "foo"
    foo.mkdir()
    b = foo / "b.py"
    a.write_text("a")
    b.write_text("b")

    test_a = test / "test_a.py"
    test_foo = test / "foo"
    test_foo.mkdir()
    test_b = test_foo / "test_b.py"
    test_a.write_text("test_a")
    test_b.write_text("test_b")

    assert bouillon.check_for_test_files(src, test)


def test_find_requirements():
    pass
