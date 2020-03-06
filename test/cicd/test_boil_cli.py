#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.

import subprocess

"""
We do a dry run test of all our commands to verify that the cli basically works
but we do not want to excute the commands, that should be done in the test
pipeline. This helps us to avoid situation where we mess up the arguments in
our cli or some other trivial mistakes.
"""


def test_boil_setup():
    subprocess.run('python boil --dry-run setup', shell=True, check=True)


def test_boil_test():
    subprocess.run('python boil --dry-run test', shell=True, check=True)


def test_boil_build():
    subprocess.run('python boil --dry-run build', shell=True, check=True)


def test_boil_train():
    pass
    # subprocess.run('python boil --dry-run train', shell=True, check=True)


def test_boil_upgrade():
    subprocess.run('python boil --dry-run upgrade', shell=True, check=True)


def test_boil_release():
    subprocess.run('python boil --dry-run release', shell=True, check=True)


def test_boil_clean():
    pass
    # subprocess.run('python boil --dry-run clean', shell=True, check=True)
