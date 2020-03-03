#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

# Contains various helpers


import shutil
import subprocess
import typing


def run(args: typing.List[str], verbose: bool, dry_run: bool,
        **kwargs) -> None:

    if verbose or dry_run:
        print('>> Command to execute: ' + str(' ').join(args))

    if dry_run:
        return

    try:
        subprocess.run(args, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        exit(e.returncode)


def check_for_test_files(src_paths: typing.List[str],
                         test_paths: typing.List[str]) -> None:

    if len(src_paths) != len(test_paths):
        raise Exception('Not all src files have a test file')

    # Todo find the missing file(s)


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
