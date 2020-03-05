#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
from pkg_resources import get_distribution

from bouillon.bouillon import run
from bouillon.bouillon import check_for_test_files
from bouillon.bouillon import repository_name


__version__ = get_distribution(__name__).version

__all__ = ('run', 'check_for_test_files', 'repository_name')
