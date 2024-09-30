# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Various helpers.

Contains various helper functions that are intended to be usefull when writing
scripts for managing (build, test, release etc.) a project.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def run(
    args: list[str],
    *,
    dry_run: bool = False,
    shell: bool = False,
    **kwargs,
) -> subprocess.CompletedProcess:
    """Run a command.

    Wrapper around subprocess.run, kwargs are forwarded to subprocess.run,
    dry_run = True, do not execute commands that make changes.
    """
    if shell:
        logger.warning("setting shell to True can cause problems.")

    logger.info(f' executing (dry-run={dry_run}): {" ".join(args)}')

    if shutil.which(args[0]) is None:
        logger.error(f'Command "{args[0]}" was not found.')

    if dry_run:
        return subprocess.CompletedProcess(
            args, 2, "dry-run output", "dry-run error")

    return subprocess.run(args, shell=shell, **kwargs)


def check_for_test_files(
    src_path: str,
    test_path: str,
    *,
    prefix: str = "test_",
    suffix: str = ".py",
    ignore: list[str] = ["__init__.py"],
) -> bool:
    """Check for test files.

    Check that all source files, all files in src_path with the defined suffix,
    have a correponding test file in the test_path with the defined prefix and
    suffix.
    """
    assert Path(src_path).exists(), f"path does not exist {src_path}"
    assert Path(test_path).exists(), f"path does not exist {test_path}"

    # Find all source files
    srcs = Path(src_path).rglob(f"*{suffix}")
    relative_srcs = list(map(lambda s: s.relative_to(src_path), srcs))
    if len(relative_srcs) == 0:
        logger.warning("No source files found.")

    # Find all test files
    tests = Path(test_path).rglob(f"{prefix}*{suffix}")
    relative_tests = map(lambda t: t.relative_to(test_path), tests)

    # Remove all tests files from the list of source files
    for t in relative_tests:
        relative_srcs.remove(Path(str(t).replace(prefix, "")))

    if len(relative_srcs) == 0:
        return True

    logger.warning(f"Missing tests for files: {relative_srcs}")
    return False
