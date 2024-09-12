#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""
Various helpers.

Contains various helper functions that are intended to be usefull when writing
scripts for managing (build, test, release etc.) a project.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path


def run(
    args: list[str],
    *,
    dry_run: bool = False,
    **kwargs
) -> subprocess.CompletedProcess:
    """
    Run a command.

    Wrapper around subprocess.run, kwargs are forwarded to subprocess.run,
    dry_run = True, do not execute commands that make changes.
    """
    logger = logging.getLogger(__name__)

    if 'shell' in kwargs and kwargs['shell'] is True:
        logger.warning('setting shell to True can cause problems.')

    logger.info(f' executing: {str(" ").join(args)}')

    if shutil.which(args[0]) is None:
        logger.error(f'Command "{args[0]}" was not found.')

    if dry_run:
        return subprocess.CompletedProcess(
            args, 2, 'dry-run output', 'dry-run error')

    return subprocess.run(args, **kwargs)


def check_for_test_files(
    src_path: str,
    test_path: str,
    *,
    prefix: str = 'test_',
    suffix: str = '.py'
) -> bool:
    """
    Check for test files.

    Check that all source files, all files in src_path with the defined suffix,
    have a correponding test file in the test_path with the defined prefix and
    suffix.
    """
    assert os.path.exists(src_path), f'path does not exist {src_path}'
    assert os.path.exists(test_path), f'path does not exist {test_path}'

    logger = logging.getLogger(__name__)

    # Find all source files
    srcs = Path(src_path).rglob(f"*{suffix}")
    relative_srcs = list(map(lambda s: s.relative_to(src_path), srcs))
    if len(relative_srcs) == 0:
        logger.warning('No source files found.')

    # Find all test files
    tests = Path(test_path).rglob(f"{prefix}*{suffix}")
    relative_tests = map(lambda t: t.relative_to(test_path), tests)

    # Remove all tests files from the list of source files
    for t in relative_tests:
        relative_srcs.remove(Path(str(t).replace(prefix, "")))

    if len(relative_srcs) == 0:
        return True

    logger.warning(f'Missing tests for files: {relative_srcs}')
    return False
