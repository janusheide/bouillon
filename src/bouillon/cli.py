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

import os
import shutil
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace,
)
from logging import basicConfig, getLevelName, getLogger
from typing import Callable

from packaging.version import InvalidVersion, Version

try:
    from tomllib import load  # type: ignore
except ModuleNotFoundError:
    from tomli import load  # type: ignore

from bouillon import git, run

logger = getLogger(__name__)


def build(*, build_steps: list[list[str]], dry_run: bool, **kwargs) -> None:
    """Build distributeables."""
    logger.info("Building source and binary distributions")
    [run(step, dry_run=dry_run) for step in build_steps]


def clean(*, distribution_dir: str, dry_run: bool, **kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info(f"Deleting {distribution_dir} directories.")
    if not dry_run:
        shutil.rmtree(distribution_dir, ignore_errors=True)


def release(
    *,
    check_branch: bool,
    releaseable_branch: str,
    version: str,
    distribution_dir: str,
    news_files: list[str],
    lint_steps: list[list[str]],
    test_steps: list[list[str]],
    dry_run: bool,
    **kwargs,
) -> None:
    """Release the project."""
    try:
        if str(Version(version)) in git.tags():
            logger.error("Tag already exists.")
            sys.exit(1)
    except InvalidVersion:
        logger.exception("Provided version is not a valid version identifier")
        sys.exit(1)

    logger.info("Running lint and test steps")
    clean(distribution_dir=distribution_dir, dry_run=dry_run, **kwargs)
    [run(step, dry_run=dry_run, check=True) for step in lint_steps]
    [run(step, dry_run=dry_run, check=True) for step in test_steps]

    if releaseable_branch not in ["*", git.current_branch()]:
        logger.error(f"Only release from the default branch {releaseable_branch}")
        sys.exit(1)

    if check_branch:
        if not git.working_directory_clean():
            logger.error("Unstaged changes in the working directory.")
            sys.exit(1)
        if not git.working_directory_updated():
            logger.error("Branch is behind remote.")
            sys.exit(1)

    logger.info("Opening the news file(s) for edit and make a commit.")
    EDITOR = os.environ.get("EDITOR", "nano")
    [run([EDITOR, file], dry_run=dry_run) for file in news_files]
    [run(["git", "add", file], dry_run=dry_run) for file in news_files]
    run(["git", "commit", "-m", f"preparing release {version}"], dry_run=dry_run)

    logger.info("Create an annotated tag, used by setuptools_scm.")
    run(["git", "tag", "-a", f"{version}", "-m",
        f"creating tag {version} for new release"], dry_run=dry_run)

    build(dry_run=dry_run, **kwargs)

    logger.info("upload builds to pypi and push commit and tag to repo.")
    try:
        run(["twine", "upload", f"{distribution_dir}/*"], dry_run=dry_run, check=True)
    except Exception:
        logger.exception("Upload failed, cleaning")
        run(["git", "tag", "-d", f"{version}"], dry_run=dry_run)
        run(["git", "reset", "--hard", "HEAD~1"], dry_run=dry_run)
        sys.exit(1)

    run(["git", "push"], dry_run=dry_run)
    run(["git", "push", "origin", f"{version}"], dry_run=dry_run)


class InputOverwrites(list):
    """Avoid copying default argument(s), when appending inputs."""

    def __copy__(self) -> list:
        """Copy."""
        return []


def cli(args) -> Namespace:
    """Build the cli."""
    parser = ArgumentParser(
        description="Bouillon",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--infile",
        default="pyproject.toml",
        type=FileType("rb"),
        help="path to input file",
    )

    infile = parser.parse_args(["-i", "pyproject.toml"]).infile
    bouillon_settings = load(infile).get("tool", {}).get("bouillon", {})
    infile.close()

    subparsers = parser.add_subparsers(help="available sub commands")

    parser_build = subparsers.add_parser("build", help="build.",
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser_build.set_defaults(function=build)
    parser_build.add_argument(
        "--build-steps", type=str, help="build steps.",
        nargs="*", action="append",
        default=InputOverwrites(bouillon_settings.get(
            "build_steps", [["python", "-m", "build"]])))

    parser_clean = subparsers.add_parser("clean", help="clean temp files.",
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser_clean.set_defaults(function=clean)
    parser_clean.add_argument(
        "--distribution-dir", type=str, help="distribution directory.",
        default=bouillon_settings.get("distribution_dir", "dist"))

    parser_release = subparsers.add_parser("release", help="release me.",
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="""
        1. Check that the choosen tag is valid and does not already exists.
        2. Cleans the distribution folder.
        3. Run all linters.
        4. Run tests.
        5. Check that we are ok to release from current branch.
        6. Check that there are no unstaged changes on the current branch.
        7. Check that the current branch is not behind the remote.
        8. Opens all news files for editing.
        9. Add and commit all news files.
        10. Creates the tag.
        11. Build the project.
        12. Uploads to pypi.
        13. Push the commit and tag to the origin.

        Note that precedence of settings in decreasing order is as follows:
        commandline arguments -> project file (pyproject.toml) -> defaults.
        """)
    parser_release.add_argument("version", type=str,
                                help="release version (e.g. '1.2.3').")
    parser_release.add_argument(
        "--check-branch", action="store_false",
        help="check that the branch is clean and up to date with remote.",
        default=bouillon_settings.get("check_branch", True))
    parser_release.add_argument(
        "--releaseable-branch", type=str,
        help="branches from which release is allowed ('*' for any branch)",
        default=bouillon_settings.get("releaseable_branch", git.default_branch()))
    parser_release.add_argument(
        "--distribution-dir", type=str, help="distribution directory.",
        default=bouillon_settings.get("distribution_dir", "dist"))
    parser_release.add_argument(
        "--news-files", type=str, help="news files to open for edits.",
        nargs="*", action="extend",
        default=InputOverwrites(bouillon_settings.get("news_files", ["NEWS.rst"])))
    parser_release.add_argument(
        "--build-steps", type=str, help="build steps.",
        nargs="*", action="append",
        default=InputOverwrites(bouillon_settings.get(
            "build_steps", [["python", "-m", "build"]])))
    parser_release.add_argument(
        "--lint-steps", type=str, help="lint steps.",
        nargs="*", action="append",
        default=InputOverwrites(bouillon_settings.get(
            "lint_steps", [["brundle"], ["licensecheck", "--zero"]])))
    parser_release.add_argument(
        "--test-steps", type=str, help="list of test steps.",
        nargs="*", action="append",
        default=InputOverwrites(bouillon_settings.get("test_steps", [["pytest"]])))

    parser_release.set_defaults(function=release)

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICIAL"],
        default="WARNING", help="set log level.")
    parser.add_argument(
        "--log-file", type=str, help="set log file.")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="perform a dry run, its helpfull to also set the log-level.")

    def _print_help(**kwargs) -> None:
        parser.print_help()

    parser.set_defaults(check=True, function=_print_help)
    return parser.parse_args(args)


def main(*, function: Callable, log_level: str, log_file: str, **kwargs) -> None:
    """Setup logging and run a step."""
    basicConfig(
        filename=log_file,
        level=getLevelName(log_level),
    )
    logger.info(f"Running {function.__name__} step, with the argumnts: {kwargs}")
    function(**kwargs)


def main_cli() -> None:
    """Main cli."""
    main(**vars(cli(sys.argv[1:])))


if __name__ == "__main__":
    main_cli()
