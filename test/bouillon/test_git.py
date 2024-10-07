# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import pytest

from bouillon import git


def test_repository_name():
    assert git.repository_name() == "bouillon"


@pytest.mark.cicd
def test_working_directory_clean():
    """Note will fail if there are unstaged changes in the working dir."""
    assert git.working_directory_clean()


@pytest.mark.cicd
def test_working_directory_updated():
    """Note will fail if not up to date with origin."""
    assert git.working_directory_updated()


def test_current_branch():
    assert isinstance(git.current_branch(), str)


def test_default_branch():
    """28/09/24 Note that this return None on a gitub runner."""
    assert git.default_branch() in ["main", None]


def test_commit_id():
    assert len(git.commit_id()) == 40


def test_tags():
    assert "0.0.1" in git.tags()
    assert "1.0.0" in git.tags()
    assert "1.4.0" in git.tags()
