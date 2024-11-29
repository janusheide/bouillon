# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import bouillon


def test_version():
    assert(bouillon.__version__)


def test_name():
    assert(bouillon.__name__ == "bouillon")


def test_run():
    bouillon.run(["ls"] )
    bouillon.run(["ls"], dry_run=True)
    bouillon.run(["unknown"], dry_run=True)


def test_find_requirements():
    pass
