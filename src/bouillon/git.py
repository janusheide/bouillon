# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Git checks, non of them changes state."""

from __future__ import annotations

from pathlib import Path
from subprocess import PIPE, STDOUT, CalledProcessError

from bouillon import run


def repository_name() -> str:
    """Get git repository name."""
    r = run(["git", "config", "--get", "remote.origin.url"],
            stdout=PIPE,
            check=True)

    return Path(r.stdout.decode().rstrip()).stem


def current_branch() -> str:
    """Get git current branch."""
    r = run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=PIPE,
            check=True)

    return r.stdout.decode().rstrip()


def default_branch() -> str | None:
    """Get git default branch, returns None if it cannot be determined."""
    try:
        r = run(["git", "rev-parse", "--abbrev-ref", "origin/HEAD"],
            stdout=PIPE,
            check=True)
        return r.stdout.decode().rstrip().lstrip("origin/")

    except CalledProcessError:
        return None


def working_directory_clean() -> bool:
    """Check if the working directory is clean."""
    try:
        run(["git", "diff", "--quiet", "--exit-code"],
            stdout=PIPE,
            check=True)
        return True

    except CalledProcessError:
        return False


def working_directory_updated() -> bool:
    """Check if the local working directory is up to date with the remote."""
    try:
        r = run(["git", "fetch", "--dry-run"],
            stdout=PIPE,
            stderr=STDOUT,
            check=True)
    except CalledProcessError:
        return False

    return r.stdout.decode().rstrip() == ""


def commit_id() -> str:
    """Get current git commit id."""
    r = run(["git", "rev-parse", "HEAD"],
            stdout=PIPE,
            check=True)

    return r.stdout.decode().rstrip()


def tags() -> list[str]:
    """Get list of all git tags."""
    r = run(["git", "tag"],
            stdout=PIPE,
            check=True)

    return r.stdout.decode().rstrip()
