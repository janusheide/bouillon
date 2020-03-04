#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.


# from src import bouillon
import bouillon


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == 'bouillon')


def test_run():
    bouillon.run("ls", verbose=True, dry_run=True)
    bouillon.run("ls", verbose=False, dry_run=False)


def test_check_for_test_files(tmpdir):
    src = tmpdir.mkdir('src')
    a = src.mkdir('foo').join('a.py')

    # src.mkdir('bar')

    test = tmpdir.mkdir('test')
    # test.mkdir('foo').join('test_a.py')
    # test.mkdir('bar')

    print(src)
    print(a)

    bouillon.check_for_test_files(src, test)


def test_get_repository_name():
    pass
    # assert(bouillon.get_repository_name() == 'bouillon')


def test_find_requirements():
    pass
