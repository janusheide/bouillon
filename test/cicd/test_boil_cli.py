#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import subprocess

"""
We do a dry run test of some of our commands to verify that the cli basically
works but we do not want to excute the commands, that should be done in the
test pipeline. This helps us to avoid situation where we mess up the arguments
in our cli or some other trivial mistakes.
"""


def test_boil_setup():
    pass


def test_boil_test():
    pass


def test_boil_build():
    subprocess.run(['python', 'boil', '--dry-run', 'build'], check=True)


def test_boil_train():
    pass
    # subprocess.run('python', 'boil', '--dry-run', 'train', check=True)


def test_boil_upgrade():
    subprocess.run(['python', 'boil', '--dry-run', 'upgrade'], check=True)


def test_boil_release():
    subprocess.run(['python', 'boil', '--dry-run', 'release', '0.0.1'],
                   check=True)


def test_boil_clean():
    pass
    # subprocess.run('python boil --dry-run clean', check=True)
