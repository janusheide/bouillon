#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue heide 2020

import glob
import subprocess


def find_requirements_files():
    return glob.glob('**/*requirements.txt', recursive=True)


def check_environment_modules(requirement_files):
    for r in requirement_files:
        subprocess.run(
            f'requirementz --file {r}',
            shell=True,
            check=True
        )


def check_module_licenses(requirement_files):
    for r in requirement_files:
        subprocess.run(
            f'liccheck -s cicd/licenses.ini -r {r}',
            shell=True,
            check=True
        )


def update_requirements_files(requirement_files):
    for r in requirement_files:
        subprocess.run(f"pur -r {r}", shell=True, check=True)


def check_for_test_files(src_path, test_path):
    pass
