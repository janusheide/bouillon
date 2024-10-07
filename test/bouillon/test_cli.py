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


def test_cli():
    assert cli(sys.argv[1:])

    with pytest.raises(SystemExit):
        assert cli(["release", "--help"])

    a = vars(cli(["release", "1.2.3"]))
    assert a["check_branch"]
    assert a["releaseable_branch"] in ["main", None]  # None on github runners
    assert a["distribution_dir"] == "dist"
    assert a["news_files"] == ["NEWS.rst",]
    assert a["build_steps"] == [["python", "-m", "build"],]
    assert a["lint_steps"] == [["brundle"],]
    assert a["test_steps"] == [["pytest"],]


def test_cli_news_files():
    a = vars(cli(["release", "100", "--news-files", "foo", "bar", "--news-files", "foobars"]))
    assert a["news_files"] == ["foo", "bar", "foobars"]

    a = vars(cli(["release", "100", "--news-files"]))
    assert a["news_files"] == []


def test_cli_lint_steps():
    a = vars(cli(["release", "100", "--lint-steps", "foo", "bar", "--lint-steps", "foo"]))
    assert a["lint_steps"] == [["foo", "bar"],["foo"]]


def test_cli_test_steps():
    a = vars(cli(["release", "100", "--test-steps", "foobar"]))
    assert a["test_steps"] == [["foobar"],]


def test_cli_build_steps():
    a = vars(cli(["release", "100", "--build-steps", "barfoo"]))
    assert a["build_steps"] == [["barfoo"],]


def test_release_invalid_version():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "fo0"])))


def test_release_existing_version():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "1.0.0"])))


def test_release_from_disallowed_branch():
    with pytest.raises(SystemExit):
        release(**vars(cli(["--dry-run", "release", "100.0.0",
                            "--releaseable-branch", "foo",])))


def test_release_unclean_branch_ok():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*", "--check-branch"])))


@pytest.mark.cicd
def test_release_unclean_branch_ok_2():
    """Note fails if branch is behind remote or not clean."""
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*"])))


def test_release_append_news_file():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*", "--check-branch", "--news-files", "pyproject.toml"])))


def test_release_append_build_step():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*", "--check-branch", "--build-steps", "build"])))


def test_release_append_lint_step():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*", "--check-branch", "--lint-steps", "brundle"])))


def test_release_append_test_step():
    release(**vars(cli(["--dry-run", "release", "100.0.0",
        "--releaseable-branch", "*", "--check-branch", "--test-steps", "pytest"])))


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
    subprocess.run(["bouillon", "clean"], check=True)
