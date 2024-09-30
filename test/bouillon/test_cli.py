# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import subprocess

import pytest

"""
We do a dry run test of some of our commands to verify that the cli basically
works but we do not want to excute the commands, that should be done in the
test pipeline. This helps us to avoid situation where we mess up the arguments
in our cli or some other trivial mistakes.
"""


def test_boil_help():
    subprocess.run(["bouillon"], check=True)


def test_boil_build():
    subprocess.run(["bouillon", "--dry-run", "build"], check=True)


def test_boil_release():
    subprocess.run(["bouillon", "--dry-run", "release", "100.9.9"], check=True)


def test_boil_release_existing_version():
    with pytest.raises(Exception):
        subprocess.run(["bouillon", "--dry-run", "release", "1.0.0"], check=True)


def test_boil_release_from_non_default_branch():
    with pytest.raises(Exception):
        subprocess.run(["bouillon", "release", "100.0.0"], check=True)


def test_boil_release_invalid_version():
    with pytest.raises(Exception):
        subprocess.run(["bouillon", "--dry-run", "release", "foo"], check=True)


def test_boil_clean():
    subprocess.run(["bouillon", "--dry-run", "clean"], check=True)
