#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

# Contains various helpers

import glob
import shutil
import subprocess
import typing


def find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def check_for_test_files(src_paths: str, test_paths: str) -> None:

    if len(src_paths) != len(test_paths):
        raise Exception('Not all src files have a test file')

    # Todo find the missing file(s)


def get_repository_name() -> str:
    raise Exception('Get repo name not implmented')
    # return .__name__


def get_commit_id() -> str:
    raise Exception('Get commit Id not implemented')
    # return .__name__


def docker_build_release(image: str, tag: str, registry: str) -> None:

    if shutil.which('docker') is None:
        raise Exception(
            '"docker" command was not found, verify that Docker is installed.')

    subprocess.run(
        f'docker build -t {image} .',
        shell=True,
        check=True
    )

    subprocess.run(
        f'docker tag {image} {registry}/{image}:{tag}',
        shell=True,
        check=True
    )

    subprocess.run(
        f'docker push {registry}/{image}:{tag}',
        shell=True,
        check=True
    )


def upgrade_bouillion() -> None:
    raise Exception('Upgrade of Bouillion not implemented')
