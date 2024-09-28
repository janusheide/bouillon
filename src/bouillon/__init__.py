# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Import bouillon functions."""


from importlib.metadata import PackageNotFoundError, version

from bouillon.bouillon import check_for_test_files, run
from bouillon.git import (
    commit_id, current_branch, default_branch, repository_name, tags,
    working_directory_clean,
)

try:
    __version__ = version("bouillon")
except PackageNotFoundError:
    pass

__all__ = ("run",
           "check_for_test_files",
           "repository_name",
           "working_directory_clean",
           "current_branch",
           "default_branch",
           "commit_id",
           "tags")
