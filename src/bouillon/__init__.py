#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

from __future__ import absolute_import
from pkg_resources import get_distribution

from bouillon.bouillon import run
from bouillon.bouillon import check_for_test_files
from bouillon.bouillon import git_repository_name
from bouillon.bouillon import git_commit_id
from bouillon.bouillon import git_tags


__version__ = get_distribution(__name__).version

__all__ = ('run', 'check_for_test_files', 'git_repository_name',
           'git_commit_id', 'git_tags')
