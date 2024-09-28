# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Git related stuff."""


from __future__ import annotations

import os
import subprocess

from bouillon import run


def repository_name() -> str:
    """Get git repository name."""
    r = run(["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            check=True)

    return os.path.split(r.stdout.decode().rstrip())[-1].split(".")[0]


def current_branch() -> str:
    """Get git current branch."""
    r = run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=subprocess.PIPE,
            check=True)

    return r.stdout.decode().rstrip()


def default_branch() -> str:
    """Get git default branch."""
    r = run(["git", "name-rev", "--name-only", "origin/HEAD"],
            stdout=subprocess.PIPE,
            check=True)

    return r.stdout.decode().rstrip().lstrip("origin/")


def working_directory_clean() -> bool:
    """Check if the working directory is clean."""
    r = run(["git", "diff", "--quiet", "--exit-code"],
            stdout=subprocess.PIPE,
            check=True)

    return not r.returncode


def commit_id() -> str:
    """Get current git commit id."""
    r = run(["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            check=True)

    return str(r.stdout.decode().rstrip())


def tags() -> list[str]:
    """Get list of all git tags."""
    r = run(["git", "tag"],
            stdout=subprocess.PIPE,
            check=True)

    return r.stdout.decode().rstrip().split("\n")
