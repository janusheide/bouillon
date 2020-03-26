#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Import bouillon functions."""

from __future__ import absolute_import
from pkg_resources import get_distribution

from bouillon.bouillon import run
from bouillon.bouillon import check_for_test_files
from bouillon.git import repository_name
from bouillon.git import working_directory_clean
from bouillon.git import current_branch
from bouillon.git import commit_id
from bouillon.git import tags


__version__ = get_distribution(__name__).version

__all__ = ('run',
           'check_for_test_files',
           'repository_name',
           'working_directory_clean',
           'current_branch',
           'commit_id',
           'tags')
