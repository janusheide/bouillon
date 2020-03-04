#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.

# Contains various helpers

import glob
import os
import shutil
import subprocess
import typing


def run(args: typing.List[str], verbose: bool, dry_run: bool,
        **kwargs) -> None:

    assert len(args) > 0, 'No arguments provided'

    if verbose or dry_run:
        print('>> Command to execute: ' + str(' ').join(args))

    if dry_run:
        return

    try:
        subprocess.run(args, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        exit(e.returncode)


def check_for_test_files(src_path, test_path, prefix='test_') -> bool:

    assert os.path.exists(src_path), f'path does not exist {src_path}'
    assert os.path.exists(test_path), f'path does not exist {test_path}'

    print('>> Looking for test files')

    print(os.path.join(src_path, '**/*.py'))
    srcs = glob.glob(os.path.join(src_path, '**/*.py'), recursive=True)
    tests = glob.glob(os.path.join(test_path, '**/test_*.py'), recursive=True)

    assert len(srcs) > 0, f'No files found in src_path: {src_path}'
    assert len(tests) > 0

    relative_tests = map(lambda t: os.path.relpath(t, test_path), tests)
    relative_srcs = map(lambda s: os.path.relpath(s, src_path), srcs)

    missing = 0

    for s in relative_srcs:
        for t in relative_tests:
            if s in t.replace(prefix, ''):
                break
            else:
                missing = missing + 1
                print(f'Not test file for {s}')
                return False

    if missing > 0:
        raise Exception(f'Missing test files for {missing} source files')

    print('should not happen')
    return True


def get_repository_name() -> str:
    raise Exception('Get repo name not implmented')
    # return .__name__


def get_commit_id() -> str:
    raise Exception('Get commit Id not implemented')
    # return .__name__


def docker_build_release(image: str, tag: str, registry: str,
                         **kwargs) -> None:

    if shutil.which('docker') is None:
        raise Exception(
            '"docker" command was not found, verify that Docker is installed.')

    run([f'docker build -t {image} .'], **kwargs)
    run([f'docker tag {image} {registry}/{image}:{tag}'], **kwargs)
    run([f'docker push {registry}/{image}:{tag}'], **kwargs)
