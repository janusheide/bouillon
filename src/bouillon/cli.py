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
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace,
)
from typing import Callable, List

from packaging.version import InvalidVersion, Version

try:
    from tomllib import load  # type: ignore
except ModuleNotFoundError:
    from tomli import load  # type: ignore

from bouillon import git, run

logger = logging.getLogger(__name__)


def build(*, build_steps: List[List[str]], dry_run: bool, **kwargs) -> None:
    """Build distributeables."""
    logger.info("Building source and binary distributions")
    for step in build_steps:
        run(step, dry_run=dry_run)


def clean(*, distribution_dir: str, dry_run: bool, **kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info(f"Deleting {distribution_dir} directories.")
    if not dry_run:
        shutil.rmtree(distribution_dir, ignore_errors=True)


def release(
    *,
    check_clean_branch: bool,
    releaseable_branch: str,
    version: str,
    distribution_dir: str,
    news_files: List[str],
    lint_steps: List[List[str]],
    test_steps: List[List[str]],
    dry_run: bool, **kwargs) -> None:
    """Release the project."""

    try:
        if str(Version(version)) in git.tags():
            logger.error("Tag already exists.")
            exit(1)
    except InvalidVersion:
        logger.error("Provided version is not a valid version identifier")
        exit(1)

    if releaseable_branch not in ["*", git.current_branch()]:
        logger.error(f"Only release from the default branch {git.default_branch()}")
        exit(1)

    clean(distribution_dir=distribution_dir, dry_run=dry_run, **kwargs)
    [run(step, dry_run=dry_run, check=True) for step in lint_steps]
    [run(step, dry_run=dry_run, check=True) for step in test_steps]

    # Check for modifications after linters
    if check_clean_branch and not git.working_directory_clean():
        logger.error("Unstaged changes in the working directory.")
        if not dry_run:
            exit(1)

    logger.info("Opening the news file(s) for edit using default editor or nano.")
    EDITOR = os.environ.get("EDITOR", "nano")
    [run([EDITOR, file], dry_run=dry_run) for file in news_files]

    logger.info("Running lint steps(s)")
    run(["git", "add"] + news_files, dry_run=dry_run)
    logger.info("Running test steps(s)")
    run(["git", "commit", "-m", f"preparing release {version}"], dry_run=dry_run)

    logger.info("Create an annotated tag, used by setuptools_scm.")
    run(["git", "tag", "-a", f"{version}", "-m",
        f"creating tag {version} for new release"], dry_run=dry_run)

    build(dry_run=dry_run, **kwargs)

    logger.info("upload builds to pypi and push commit and tag to repo.")
    try:
        run(["twine", "upload", f"{distribution_dir}/*"], dry_run=dry_run, check=True)
    except Exception as e:
        logger.error(f"Upload failed with error {e}, cleaning")
        run(["git", "tag", "-d", f"{version}"], dry_run=dry_run)
        run(["git", "reset", "--hard", "HEAD~1"], dry_run=dry_run)
        exit(1)

    run(["git", "push"], dry_run=dry_run)
    run(["git", "push", "origin", f"{version}"], dry_run=dry_run)


class input_overwrites(list):
    """Avoid copying default argument(s), when appending inputs."""
    def __copy__(self):
        return []


def cli(args) -> Namespace:
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
        default="pyproject.toml",
        type=FileType("rb"),
        help="Path to input file",
    )

    bouillon_settings = load(
        parser.parse_args(["-i", "pyproject.toml"]).infile).get(
            "tool", dict()).get("bouillon", dict())
#
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICIAL"],
        default="WARNING", help="Set log level.")
    parser.add_argument(
        "--log-file", type=str, help="Set log file.")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Perform a dry run, its helpfull to also set the log-level.")

    subparsers = parser.add_subparsers(help="Available sub commands")

    parser_build = subparsers.add_parser("build", help="Build.",
        formatter_class=ArgumentDefaultsHelpFormatter,)
    parser_build.set_defaults(function=build)
    parser_build.add_argument(
        "--build_steps", type=List[str], help="List of build steps.",
        default=bouillon_settings.get("build_steps", [["python", "-m", "build"],]))

    parser_clean = subparsers.add_parser("clean", help="Clean temp files.",
        formatter_class=ArgumentDefaultsHelpFormatter,)
    parser_clean.set_defaults(function=clean)
    parser_clean.add_argument(
        "--distribution_dir", type=str, help="Distribution directory.",
        default=bouillon_settings.get("distribution_dir", "dist"))

    parser_release = subparsers.add_parser("release", help="release me.",
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="""
        1. Check that the choosen tag does not already exists.
        2. Check that we are releasing from the default_branch.
        3. Check that there are no unstaged changes on the current branch.
        4. Cleans the distribution folder.
        5. Run all linters.
        6. Run tests.
        7. Opens all news files for editing.
        8. Add and commit all news files.
        9. Creates the tag.
        10. Build the project.
        11. Uploads to pypi.
        12. Push the commit and tag to the origin.

        Note that precedence of settings in decreasing order is as follows:
        commandline arguments -> project file (pyproject.toml) -> defaults.
        """
        )
    parser_release.add_argument("version", type=str,
                                help="release version (e.g. '1.2.3').")
    parser_release.add_argument(
        "--check_clean_branch", action="store_false",
        help="Check that the current branch is clean.",
        default=bouillon_settings.get("check_clean_branch", True))
    parser_release.add_argument(
        "--releaseable_branch", type=str,
        help="Branches from which release is allowed ('*' for any branch)",
        default=bouillon_settings.get("releaseable_branch", git.default_branch()))
    parser_release.add_argument(
        "--distribution_dir", type=str, help="Distribution directory.",
        default=bouillon_settings.get("distribution_dir", "dist"))
    parser_release.add_argument(
        "--news_files", type=str, help="News files to open for edits.",
        nargs="+", action="extend",
        default=input_overwrites(bouillon_settings.get("news_files", ["NEWS.rst",])))
    parser_release.add_argument(
        "--build_steps", type=str, help="List of build steps.",
        nargs="+", action="append",
        default=input_overwrites(bouillon_settings.get("build_steps", [["python", "-m", "build"],])))
    parser_release.add_argument(
        "--lint_steps", type=str, help="List of lint steps.",
        nargs="+", action="append",
        default=input_overwrites(bouillon_settings.get("lint_steps", [["brundle"],])))
    parser_release.add_argument(
        "--test_steps", type=str, help="List of test steps.",
        nargs="+", action="append",
        default=input_overwrites(bouillon_settings.get("test_steps", [["pytest"],])))

    parser_release.set_defaults(function=release)
    return parser.parse_args(args)


def main(*, function: Callable, log_level: str, log_file: str, **kwargs) -> None:
    """Setup logging and run a step."""
    logging.basicConfig(filename=log_file, level=log_level)
    logger.info(f"Running {function.__name__} step, with the argumnts: {kwargs}")
    function(**kwargs)


def main_cli() -> None:
    main(**vars(cli(sys.argv[1:])))


if __name__ == "__main__":
    main_cli()
