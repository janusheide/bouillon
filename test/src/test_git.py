#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import bouillon


def test_repository_name():
    assert bouillon.git.repository_name() == 'bouillon'


def test_working_directory_clean(tmpdir):
    bouillon.run(['git', 'stash'])
    assert bouillon.git.working_directory_clean() == True
    bouillon.run(['git', 'stash', 'apply'])


def test_current_branch():
    assert isinstance(bouillon.git.current_branch(), str)


def test_commit_id():
    assert len(bouillon.git.commit_id()) == 40


def test_tags():
    assert '0.0.1' in bouillon.git.tags()
