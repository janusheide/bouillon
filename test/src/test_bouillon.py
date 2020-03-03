#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue heide 2020

import bouillon


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == 'bouillon')


def test_run():
    bouillon.run("ls", verbose=True, dry_run=True)
    bouillon.run("ls", verbose=False, dry_run=False)


def test_get_repository_name():
    pass
    # assert(bouillon.get_repository_name() == 'bouillon')


def test_find_requirements():
    pass
