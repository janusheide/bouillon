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

import bouillon

logger = logging.getLogger(__name__)


def test(
    *,
    cicd_tests: bool = True,
    test_files: bool = True,
    unit_tests: bool = True,
    **kwargs,
) -> None:
    """Run tests."""
    if test_files:
        if not bouillon.check_for_test_files(
            os.path.join("src", bouillon.git.repository_name()),
                os.path.join("test", bouillon.git.repository_name())):
            exit(1)

    # https://docs.pytest.org/en/latest/
    # https://pytest-cov.readthedocs.io/en/latest/
    if unit_tests:
        bouillon.run([
            "pytest",
            f'{os.path.join("test", bouillon.git.repository_name())}',
            "--cov=bouillon",
            "--cov-report",
            "term-missing",
            "--cov-fail-under=95",
            "--durations=5",
            "-vv",
            ],
            **kwargs)

    if cicd_tests:
        bouillon.run([
            "pytest",
            f'{os.path.join("test", "test_boil.py")}',
            "--durations=5",
            "-vv"],
            **kwargs)


def build(**kwargs) -> None:
    """Build distributeables."""
    logger.info("Building source and binary distributions")
    bouillon.run(["python", "-m", "build"], **kwargs)


def train(**kwargs) -> None:
    """Train a model."""
    logger.critical("train step not implemented.")


def clean(**kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info('Deleting "build" and "dist" directories.')
    shutil.rmtree("dist", ignore_errors=True)


def release(*, version: str, **kwargs) -> None:
    """Release the project."""
    if bouillon.run(["pysemver", "check", version]).returncode:
        logger.error("Provided version is not valid semver")
        exit(1)

    if not kwargs["dry_run"]:
        if bouillon.git.current_branch() != "master":
            logger.error("Only release from the master branch")
            exit(1)

        if not bouillon.git.working_directory_clean():
            logger.error("Unstaged changes in the working directory.")
            exit(1)

        if version in bouillon.git.tags():
            logger.error("Tag already exists.")
            exit(1)
    else:
        logger.debug("Skipped git status checks.")

    clean(**kwargs)
    bouillon.run(["brundle"], **kwargs)
    test(**kwargs)

    logger.debug("Edit the news file using default editor or nano.")
    EDITOR = os.environ.get("EDITOR", "nano")
    bouillon.run([EDITOR, "NEWS.rst"], **kwargs)
    bouillon.run(["git", "add", "NEWS.rst"], **kwargs)
    bouillon.run(["git", "commit", "-m", f"preparing release {version}"], **kwargs)

    logger.debug("Create an annotated tag, used by setuptools_scm.")
    bouillon.run(["git", "tag", "-a", f"{version}", "-m",
                  f"creating tag {version} for new release"], **kwargs)

    build(**kwargs)

    logger.debug("upload builds to pypi and push commit and tag to repo.")
    try:
        bouillon.run(["twine", "upload", "dist/*"], **kwargs)
    except Exception as e:
        bouillon.run(["git", "tag", "-d", f"{version}"], **kwargs)
        bouillon.run(["git", "reset", "--hard", "origin/master"], **kwargs)
        logger.error(f"Upload failed with error {e}, cleaning")
        exit(1)

    bouillon.run(["git", "push"], **kwargs)
    bouillon.run(["git", "push", "origin", f"{version}"], **kwargs)


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

    parser_test = subparsers.add_parser("test", help="Run tests")
    parser_test.set_defaults(function=test)

    parser_test.add_argument(
        "--no-test-files-check", dest="test_files", action="store_false",
        help="Do not check that for each source file there is a test file.")
    parser_test.add_argument(
        "--no-unit-tests", dest="unit_tests", action="store_false",
        help="Do not run unit tests.")
    parser_test.add_argument(
        "--no-cicd-tests", dest="cicd_tests", action="store_false",
        help="Do not run CICD tests.")

    parser_train = subparsers.add_parser("train", help="Train.")
    parser_train.set_defaults(function=train)

    parser_clean = subparsers.add_parser("clean", help="Clean temp files.")
    parser_clean.set_defaults(function=clean)

    parser_release = subparsers.add_parser("release", help="release me.")
    parser_release.add_argument("version", type=str,
                                help="release version.")
    parser_release.set_defaults(function=release)

    return parser.parse_args()


def run(*, function: Callable, log_level: str, log_file: str, **kwargs) -> None:
    """Setup logging and run a step."""
    logging.basicConfig(filename=log_file, level=log_level)
    if util.find_spec("bouillon") is None:
        logger.error('Failed to import bouillon, run "pip install .[dev]" first.')
        exit(1)

    logger.debug(f'Running "{function.__name__}" step.')
    function(**kwargs)


if __name__ == "__main__":
    args = cli()
    run(**vars(args))
