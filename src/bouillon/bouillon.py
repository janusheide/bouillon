#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue heide 2020

import glob
import subprocess


def find_requirements_files():
    return glob.glob('**/*requirements.txt', recursive=True)


def check_requirements_files(requirement_files):
    for r in requirement_files:
        subprocess.run(f"requirementz --file {r}", shell=True, check=True)


def update_requirements_files():
    pass


def check_for_test_files():
    pass