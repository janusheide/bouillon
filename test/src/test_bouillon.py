#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.


# from src import bouillon
import bouillon

# import subprocess


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == 'bouillon')


def test_run():
    bouillon.run(['ls'], )
    bouillon.run(['ls'], dry_run=True)


def test_check_for_test_files_fail(tmpdir):
    src = tmpdir.mkdir('src')
    a = src.join('a.py')
    b = src.mkdir('foo').join('b.py')
    a.write('a')
    b.write('b')

    test = tmpdir.mkdir('test')
    test_a = test.join('test_a.py')
    test_a.write('test_a')

    assert(not bouillon.check_for_test_files(src, test))


def test_check_for_test_files(tmpdir):
    src = tmpdir.mkdir('src')
    a = src.join('a.py')
    b = src.mkdir('foo').join('b.py')
    a.write('a')
    b.write('b')

    test = tmpdir.mkdir('test')
    test_a = test.join('test_a.py')
    test_b = test.mkdir('foo').join('test_b.py')
    test_a.write('test_a')
    test_b.write('test_b')

    assert(bouillon.check_for_test_files(src, test))


def test_repository_name():
    assert(bouillon.repository_name() == 'bouillon')


def test_find_requirements():
    pass
