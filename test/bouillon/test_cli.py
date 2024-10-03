# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import subprocess
import sys

import pytest

from bouillon.cli import cli, release

"""
We do a dry run test of some of our commands to verify that the cli basically
works but we do not want to excute the commands, that should be done in the
test pipeline. This helps us to avoid situation where we mess up the arguments
in our cli or some other trivial mistakes.
"""

def test_release_invalid_version():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "fo0"])))


def test_release_existing_version():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "1.0.0"])))


def test_release_from_disallowed_branch():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "100.0.0",
                            "--releaseable_branch", "foo",])))


def test_release_unclean_branch_ok():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable_branch", "*", "--check_clean_branch"])))


def test_cli():
    assert cli(sys.argv[1:])
    with pytest.raises(SystemExit):
        assert cli(["release", "--help"])

    a = vars(cli(["release", "1.2.3"]))

    assert a["check_clean_branch"]
    assert a["releaseable_branch"] in ["main", None]  # None on github runners
    assert a["distribution_dir"] == "dist"
    assert a["news_files"] == ["NEWS.rst",]
    assert a["build_steps"] == [["python", "-m", "build"],]
    assert a["lint_steps"] == [["brundle"],]
    assert a["test_steps"] == [["pytest"],]


def test_boil_help():
    subprocess.run(["bouillon"], check=True)


def test_boil_infile():
    subprocess.run(["bouillon", "-i", "pyproject.toml"], check=True)


def test_boil_build():
    subprocess.run(["bouillon", "--dry-run", "build"], check=True)


def test_boil_release_existing_version():
    with pytest.raises(Exception):
        subprocess.run(["bouillon", "--dry-run", "release", "1.0.0"], check=True)


def test_boil_release_invalid_version():
    with pytest.raises(Exception):
        subprocess.run(["bouillon", "--dry-run", "release", "foo3"], check=True)


def test_boil_clean():
    subprocess.run(["bouillon", "--dry-run", "clean"], check=True)
