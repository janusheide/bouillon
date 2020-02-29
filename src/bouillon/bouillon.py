#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

# Contains various helpers

import glob
import typing


def find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def check_for_test_files(src_paths: str, test_paths: str) -> None:

    if len(src_paths) != len(test_paths):
        raise Exception('Not all src files have a test file')

    # Todo find the missing file(s)


def get_repository_name() -> str:
    pass
    # return .__name__


def upgrade_bouillion() -> None:
    raise Exception('Upgrade of Bouillion not implemented')
