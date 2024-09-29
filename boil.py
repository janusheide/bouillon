#! /usr/bin/env python3
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""Command Line Interface (CLI) for project interaction.

Run various commands, such as; test, build, release on your project. You should
modify the steps that are relevant for your project, and the cli such that it
reflects those steps. The cli specified here is used for the bouillon module.
"""

from __future__ import annotations

import logging
import os
import shutil
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from importlib import util
from typing import Callable

from packaging.version import InvalidVersion, Version

from bouillon import git, run

logger = logging.getLogger(__name__)


def build(**kwargs) -> None:
    """Build distributeables."""
    logger.info("Building source and binary distributions")
    run(["python", "-m", "build"], **kwargs)


def clean(**kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info('Deleting "dist" directories.')
    shutil.rmtree("dist", ignore_errors=True)


def release(*, version: str, **kwargs) -> None:
    """Release the project."""
    try:
        v = Version(version)
        if v in git.tags():
            logger.error("Tag already exists.")
            exit(1)
    except InvalidVersion:
        logger.error("Provided version is not a valid version identifier")

    if not kwargs["dry_run"]:
        if git.current_branch() != git.default_branch():
            logger.error(f"Only release from the default branch {git.default_branch()}")
            exit(1)

        if not git.working_directory_clean():
            logger.error("Unstaged changes in the working directory.")
            exit(1)

    else:
        logger.debug("Skipped git status checks.")

    clean(**kwargs)
    run(["brundle"], **kwargs)
    run(["pytest"], **kwargs)

    logger.debug("Edit the news file using default editor or nano.")
    EDITOR = os.environ.get("EDITOR", "nano")
    run([EDITOR, "NEWS.rst"], **kwargs)
    run(["git", "add", "NEWS.rst"], **kwargs)
    run(["git", "commit", "-m", f"preparing release {version}"], **kwargs)

    logger.debug("Create an annotated tag, used by setuptools_scm.")
    run(["git", "tag", "-a", f"{version}", "-m",
        f"creating tag {version} for new release"], **kwargs)

    build(**kwargs)

    logger.debug("upload builds to pypi and push commit and tag to repo.")
    try:
        run(["twine", "upload", "dist/*"], **kwargs)
    except Exception as e:
        logger.error(f"Upload failed with error {e}, cleaning")
        run(["git", "tag", "-d", f"{version}"], **kwargs)
        run(["git", "reset", "--hard", "HEAD~1"], **kwargs)
        exit(1)

    run(["git", "push"], **kwargs)
    run(["git", "push", "origin", f"{version}"], **kwargs)


def cli() -> Namespace:
    """Build the cli."""
    parser = ArgumentParser(
        description="Bouillon",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(check=True, function=_print_help)

    parser.add_argument(
        "--dry-run", action="store_true", help="Perform a dry run.")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICIAL"],
        default="WARNING", help="Set log level.")
    parser.add_argument(
        "--log-file", type=str, help="Set log file.")

    subparsers = parser.add_subparsers(help="Available sub commands")

    parser_build = subparsers.add_parser("build", help="Build.")
    parser_build.set_defaults(function=build)

    parser_clean = subparsers.add_parser("clean", help="Clean temp files.")
    parser_clean.set_defaults(function=clean)

    parser_release = subparsers.add_parser("release", help="release me.")
    parser_release.add_argument("version", type=str,
                                help="release version.")
    parser_release.set_defaults(function=release)

    return parser.parse_args()


def main(*, function: Callable, log_level: str, log_file: str, **kwargs) -> None:
    """Setup logging and run a step."""
    logging.basicConfig(filename=log_file, level=log_level)
    if util.find_spec("bouillon") is None:
        logger.error('Failed to import bouillon, run "pip install .[dev]" first.')
        exit(1)

    logger.debug(f'Running "{function.__name__}" step.')
    function(**kwargs)


if __name__ == "__main__":
    args = cli()
    main(**vars(args))
