#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.

# Contains various helpers

import glob
import os
import subprocess
import typing


def run(args: typing.Any, dry_run: bool = False, verbose: bool = False,
        **kwargs: typing.Any) -> subprocess.CompletedProcess:

    if dry_run or verbose:
        print(f'Command to executed: {str(" ").join(args)}')

    if dry_run:
        return subprocess.run('true', **kwargs)

    try:
        return subprocess.run(args, **kwargs)
    except subprocess.CalledProcessError as e:
        exit(e.returncode)


def check_for_test_files(src_path: str, test_path: str, *,
                         prefix: str = 'test_', suffix: str = 'py') -> bool:
    """
    Check that all source files have a correponding test file.
    """
    assert os.path.exists(src_path), f'path does not exist {src_path}'
    assert os.path.exists(test_path), f'path does not exist {test_path}'

    # Find all soruce files
    srcs = glob.glob(os.path.join(src_path, f'**/*.{suffix}'), recursive=True)
    assert len(srcs) > 0, 'No source files found.'
    relative_srcs = list(map(lambda s: os.path.relpath(s, src_path), srcs))

    # Find all test files
    tests = glob.glob(os.path.join(test_path, f'**/test_*.{suffix}'),
                      recursive=True)
    relative_tests = map(lambda t: os.path.relpath(t, test_path), tests)
    tests_no_prefix = map(lambda t: t.replace(prefix, ''),  relative_tests)

    # Remove all tests files from the list of source files
    for t in tests_no_prefix:
        relative_srcs.remove(t)

    if len(relative_srcs) == 0:
        return True

    print(f'Missing tests for files: {relative_srcs}')
    return False


def git_repository_name(**kwargs: typing.Any) -> str:

    r = run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE,
            **kwargs)

    return os.path.split(r.stdout.decode().rstrip())[-1]


def git_commit_id(**kwargs: typing.Any) -> str:

    r = run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, **kwargs)

    return r.stdout.decode().rstrip()


def docker_build_release(*, image: str, tag: str, registry: str,
                         **kwargs: typing.Any) -> None:

    run([f'docker build -t {image} .'], **kwargs)
    run([f'docker tag {image} {registry}/{image}:{tag}'], **kwargs)
    run([f'docker push {registry}/{image}:{tag}'], **kwargs)
