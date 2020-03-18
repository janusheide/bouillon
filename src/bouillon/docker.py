#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Docker related stuff."""

import typing

import bouillon


def build_release(*, image: str, tag: str, registry: str,
                  **kwargs: typing.Any) -> None:
    """Build, tag and push docker image."""
    bouillon.run([f'docker build -t {image} .'], **kwargs)
    bouillon.run([f'docker tag {image} {registry}/{image}:{tag}'], **kwargs)
    bouillon.run([f'docker push {registry}/{image}:{tag}'], **kwargs)
