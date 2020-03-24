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

import glob
import os
import shutil
import subprocess
import typing


def run(
    args: typing.List[str],
    *,
    dry_run: bool = False,
    verbose: bool = False,
    **kwargs: typing.Any
        ) -> subprocess.CompletedProcess:
    """
    Run a command.

    Wrapper around subprocess.run, kwargs are forwarded to subprocess.run,
    verbose = True, to print the command to be executed.
    dry_run = True, to print the command to be executed instead of executing.
    """
    if 'shell' in kwargs and kwargs['shell'] is True:
        print('Warning: setting shell to True can cause problems.')

    if dry_run or verbose:
        print(f'Command to execute: {str(" ").join(args)}')

    if shutil.which(args[0]) is None:
        print(f'Command "{args[0]}" was not found.')

    if dry_run:
        return subprocess.CompletedProcess('', 0)

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

    # Find all soruce files
    srcs = glob.glob(os.path.join(src_path, f'**/*{suffix}'), recursive=True)
    assert len(srcs) > 0, 'No source files found.'
    relative_srcs = list(map(lambda s: os.path.relpath(s, src_path), srcs))

    # Find all test files
    tests = glob.glob(os.path.join(test_path, f'**/{prefix}*{suffix}'),
                      recursive=True)
    relative_tests = map(lambda t: os.path.relpath(t, test_path), tests)
    tests_no_prefix = map(lambda t: t.replace(prefix, ''), relative_tests)

    # Remove all tests files from the list of source files
    for t in tests_no_prefix:
        relative_srcs.remove(t)

    if len(relative_srcs) == 0:
        return True

    print(f'Missing tests for files: {relative_srcs}')
    return False
