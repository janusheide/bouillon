# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Various helpers.

Contains various helper functions that are intended to be usefull when writing
scripts for managing (build, test, release etc.) a project.
"""

from __future__ import annotations

import logging
import shutil
import subprocess

logger = logging.getLogger(__name__)


def run(
    args: list[str],
    *,
    dry_run: bool = False,
    shell: bool = False,
    **kwargs,
) -> subprocess.CompletedProcess:
    """Run a command.

    Wrapper around subprocess.run, kwargs are forwarded to subprocess.run,
    dry_run = True, do not execute commands that make changes.
    """
    if shell:
        logger.warning("setting shell to True can cause problems.")

    logger.info(f' executing (dry-run={dry_run}): {" ".join(args)}')

    if shutil.which(args[0]) is None:
        logger.error(f'Command "{args[0]}" was not found.')

    if dry_run:
        return subprocess.CompletedProcess(
            args, 2, "dry-run output", "dry-run error")

    return subprocess.run(args, shell=shell, **kwargs)
