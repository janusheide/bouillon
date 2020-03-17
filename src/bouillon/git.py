#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Git related stuff."""

import bouillon
import os
import subprocess
import typing


def repository_name(**kwargs: typing.Any) -> str:
    """Get git repository name."""
    r = bouillon.run(['git', 'rev-parse', '--show-toplevel'],
                     stdout=subprocess.PIPE,
                     **kwargs)

    return str(os.path.split(r.stdout.decode().rstrip())[-1])


def current_branch(**kwargs: typing.Any) -> str:
    """Get git current branch."""
    r = bouillon.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                     stdout=subprocess.PIPE,
                     **kwargs)

    return str(r.stdout.decode().rstrip())


def commit_id(**kwargs: typing.Any) -> str:
    """Get current git commit id."""
    r = bouillon.run(['git', 'rev-parse', 'HEAD'],
                     stdout=subprocess.PIPE,
                     **kwargs)

    return str(r.stdout.decode().rstrip())


def tags(**kwargs: typing.Any) -> typing.List[str]:
    """Get list of all git tags."""
    r = bouillon.run(['git', 'tag', '--list'],
                     stdout=subprocess.PIPE,
                     **kwargs)

    tags: typing.List[str] = r.stdout.decode().rstrip().split('\n')

    return tags
