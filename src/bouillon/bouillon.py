#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

# Various helpers

import glob

# import subprocess


_repository_name = 'bouillon'


def find_requirement_files():
    return glob.glob('**/*requirements.txt', recursive=True)


def check_for_test_files(src_paths, test_paths):

    if len(src_paths) != len(test_paths):
        raise Exception('Not all src files have a test file')

    # Todo find the missing file(s)


def get_repository_name():
    pass
    # return .__name__


def upgrade_bouillion():
    raise Exception('Upgrade of Bouillion not implemented')
