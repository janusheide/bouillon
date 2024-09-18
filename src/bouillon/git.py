# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Git related stuff."""


from __future__ import annotations

import os
import subprocess

import bouillon


def repository_name() -> str:
    """Get git repository name."""
    r = bouillon.run(["git", "config", "--get", "remote.origin.url"],
                     stdout=subprocess.PIPE,
                     check=True)

    return str(os.path.split(r.stdout.decode().rstrip())[-1].split(".")[0])


def current_branch() -> str:
    """Get git current branch."""
    r = bouillon.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                     stdout=subprocess.PIPE,
                     check=True)

    return str(r.stdout.decode().rstrip())


def working_directory_clean() -> bool:
    """Check if the working directory is clean."""
    r = bouillon.run(["git", "diff", "--quiet", "--exit-code"],
                     stdout=subprocess.PIPE,
                     check=True)

    return not r.returncode


def commit_id() -> str:
    """Get current git commit id."""
    r = bouillon.run(["git", "rev-parse", "HEAD"],
                     stdout=subprocess.PIPE,
                     check=True)

    return str(r.stdout.decode().rstrip())


def tags() -> list[str]:
    """Get list of all git tags."""
    r = bouillon.run(["git", "tag"],
                     stdout=subprocess.PIPE,
                     check=True)

    tags: list[str] = r.stdout.decode().rstrip().split("\n")
    return tags
