# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Import bouillon functions."""


from importlib.metadata import PackageNotFoundError, version

from bouillon import git
from bouillon.bouillon import run

try:
    __version__ = version("bouillon")
except PackageNotFoundError:
    pass

__all__ = (
    "git",
    "run",
    )
