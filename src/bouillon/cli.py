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
from argparse import (
    ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace,
)
from typing import Callable

from packaging.version import InvalidVersion, Version

try:
    from tomllib import load  # type: ignore
except ModuleNotFoundError:
    from tomli import load  # type: ignore

from bouillon import git, run

logger = logging.getLogger(__name__)


def build(*, build_steps: list[list[str]], dry_run: bool, **kwargs) -> None:

    print(kwargs)
    """Build distributeables."""
    logger.info("Building source and binary distributions")
    for step in build_steps:
        run(step, dry_run=dry_run)


def clean(*, distribution_dir: str, **kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info('Deleting "distribution_dirs" directories.')
    shutil.rmtree(distribution_dir, ignore_errors=True)


def release(
    *,
    version: str,
    distribution_dir: str,
    releaseable_branch: str,
    news_files: list[str],
    lint_steps: list[list[str]],
    test_steps: list[list[str]],
    dry_run: bool, **kwargs) -> None:
    """Release the project."""

    try:
        if str(Version(version)) in git.tags():
            logger.error("Tag already exists.")
            exit(1)
    except InvalidVersion:
        logger.error("Provided version is not a valid version identifier")
        exit(1)

    if dry_run:
        logger.debug("Skipped git status checks.")
    else:
        if releaseable_branch not in ["*", git.current_branch()]:
            logger.error(f"Only release from the default branch {git.default_branch()}")
            exit(1)

        if not git.working_directory_clean():
            logger.error("Unstaged changes in the working directory.")
            exit(1)


    clean(distribution_dir=distribution_dir, **kwargs)
    [run(step, dry_run=dry_run) for step in lint_steps]
    [run(step, dry_run=dry_run) for step in test_steps]

    logger.debug("Edit the news file using default editor or nano.")
    EDITOR = os.environ.get("EDITOR", "nano")

    [run([EDITOR, file], dry_run=dry_run) for file in news_files]
    run(["git", "add"] + news_files, dry_run=dry_run)
    run(["git", "commit", "-m", f"preparing release {version}"], dry_run=dry_run)

    logger.debug("Create an annotated tag, used by setuptools_scm.")
    run(["git", "tag", "-a", f"{version}", "-m",
        f"creating tag {version} for new release"], dry_run=dry_run)

    build(dry_run=dry_run, **kwargs)

    logger.debug("upload builds to pypi and push commit and tag to repo.")
    try:
        run(["twine", "upload", f"{distribution_dir}/*"], dry_run=dry_run)
    except Exception as e:
        logger.error(f"Upload failed with error {e}, cleaning")
        run(["git", "tag", "-d", f"{version}"], dry_run=dry_run)
        run(["git", "reset", "--hard", "HEAD~1"], dry_run=dry_run)
        exit(1)

    run(["git", "push"], dry_run=dry_run)
    run(["git", "push", "origin", f"{version}"], dry_run=dry_run)


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
        "-i",
        "--infile",
        nargs="*",
        default="pyproject.toml",
        type=FileType("rb"),
        help="Path to input file",
    )

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


default_settings = {
    "releaseable_branch": git.default_branch(),
    "distribution_dir": "dist",
    "news_files": ["NEWS.rst",],
    "build_steps": [["python", "-m", "build"],],
    "lint_steps": [["brundle"],],
    "test_steps": [["pytest"],],
}

def settings(*, infile: FileType, **kwargs) -> dict:
    """Read settings."""
    settings = default_settings

    data = load(infile) #type: ignore
    settings.update(data.get("tool", dict()).get("bouillon", dict()))
    settings.update(kwargs)
    return settings


def main(*, function: Callable, log_level: str, log_file: str, **kwargs) -> None:
    """Setup logging and run a step."""
    logging.basicConfig(filename=log_file, level=log_level)
    logger.debug(f'Running "{function.__name__}" step.')
    function(**kwargs)


def main_cli() -> None:
    args = cli()
    main(**settings(**vars(args)))


if __name__ == "__main__":
    main_cli()
