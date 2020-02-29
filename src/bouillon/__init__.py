#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
from pkg_resources import get_distribution

from bouillon.bouillon import get_repository_name
# import bouillon


__version__ = get_distribution(__name__).version
