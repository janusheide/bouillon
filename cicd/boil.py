#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

"""
Command Line Interface (CLI) for project interaction.

Run various commands, such as; test, build, release on your project. You should
modify the steps that are relevant for your project, and the cli such that it
reflects those steps. The cli specified here is used for the bouillon module.
"""

import argparse
import glob
from importlib import util
import logging
import os
import shutil
import subprocess
import typing

# Modules that are not part of 'standard' Python is only installed if they can
# be found, this allows us to run the setup step where they are installed
# without importing the modules we are about to install.
if util.find_spec('bouillon') is not None:
    import bouillon

if util.find_spec('semver') is not None:
    import semver

logger = logging.getLogger(__name__)


def find_requirement_files() -> typing.List[str]:
    """Find all requirements.txt files."""
    return glob.glob('**/*requirements.txt', recursive=True)


def setup(*, dry_run: bool, **kwargs) -> None:
    """Install dependencies. Since bouillon is also inste."""
    logger.info('Installing dependencies')

    if dry_run:
        exit(0)

    # NOTE For your project instead add bouillon to requirements.txt.
    subprocess.run(['pip', 'install', '-e', '.'], **kwargs)

    for r in find_requirement_files():
        subprocess.run(['pip', 'install', '-r', f'{r}'], **kwargs)


def test(
    *,
    cicd_tests: bool = True,
    licenses: bool = True,
    pep8: bool = True,
    requirements: bool = True,
    static: bool = True,
    test_files: bool = True,
    vulnerabilities: bool = True,
    unit_tests: bool = True,
    **kwargs
        ) -> None:
    """Run tests."""
    if pep8:
        bouillon.run(['flake8', 'src', 'cicd'], **kwargs)

    if static:
        bouillon.run(['mypy', 'src', '--config-file', 'cicd/mypy.ini'],
                     **kwargs)

    # https://pypi.org/project/Requirementz/
    if requirements:
        for r in find_requirement_files():
            bouillon.run(['requirementz', '--file', f'{r}'], **kwargs)

    # https://github.com/dhatim/python-license-check
    if licenses:
        for r in find_requirement_files():
            bouillon.run(['liccheck', '-s', 'cicd/licenses.ini', '-r', f'{r}'],
                         **kwargs)

    # https://github.com/pyupio/safety
    if vulnerabilities:
        bouillon.run(['safety', 'check'], **kwargs)

    if test_files:
        if not bouillon.check_for_test_files(
            os.path.join('src', bouillon.git.repository_name()),
                os.path.join('test', 'src')):
            exit(1)

    # https://docs.pytest.org/en/latest/
    # https://pytest-cov.readthedocs.io/en/latest/
    if unit_tests:
        bouillon.run([
            'pytest',
            f'{os.path.join("test", "src")}',
            '--cov=bouillon',
            '--cov-report',
            'term-missing',
            '--cov-fail-under=85',
            '--durations=5',
            '-vv'],
            **kwargs)

    if cicd_tests:
        bouillon.run([
            'pytest',
            f'{os.path.join("test", "cicd")}',
            '--durations=5',
            '-vv'],
            **kwargs)


def upgrade(**kwargs) -> None:
    """Upgrade the versions of the used modules."""
    # https://github.com/alanhamlett/pip-update-requirements
    for r in find_requirement_files():
        bouillon.run(['pur', '-r', f'{r}', '--force'], **kwargs)

    setup(**kwargs)


def build(**kwargs) -> None:
    """Build distributeables."""
    logger.info('Building source and binary distributions')
    bouillon.run(['python', 'setup.py', 'sdist'], **kwargs)
    bouillon.run(['python', 'setup.py', 'bdist_wheel'],
                 **kwargs)


def train(**kwargs) -> None:
    """Train a model."""
    logger.critical("train step not implemented.")


def clean(**kwargs) -> None:
    """Remove files and dirs created during build."""
    logger.info('Deleting "build" and "dist" directories.')
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)


def release(*, version: str, **kwargs) -> None:
    """Release the project."""
    logger.info('Checking that version is valid semver,')
    semver.parse(version)

    if kwargs['dry_run'] is False:
        if bouillon.git.current_branch() != 'master':
            logger.error('Only release from the master branch')
            exit(1)

        if not bouillon.git.working_directory_clean():
            logger.error('Unstaged changes in the working directory.')
            exit(1)

        if version in bouillon.git.tags():
            logger.error("Tag already exists.")
            exit(1)
    else:
        logger.debug('Skipped git status checks.')

    clean(**kwargs)
    test(**kwargs)

    logger.debug('Edit the news file using default editor or nano.')
    EDITOR = os.environ.get('EDITOR', 'nano')
    bouillon.run([EDITOR, 'NEWS.rst'], **kwargs)
    bouillon.run(['git', 'add', 'NEWS.rst'], **kwargs)
    bouillon.run(['git', 'commit', '-m', '"preparing release"'], **kwargs)

    logger.debug('Create an annotated tag, used by scm in setup.py.')
    bouillon.run(['git', 'tag', '-a', f'{version}', '-m',
                  f'creating tag {version} for new release'], **kwargs)

    build(**kwargs)

    logger.debug('upload builds to pypi and push commit and tag to repo.')
    bouillon.run(['twine', 'upload', 'dist/*'], **kwargs)
    bouillon.run(['git', 'push'], **kwargs)
    bouillon.run(['git', 'push', 'origin', f'{version}'], **kwargs)


def cli() -> typing.Any:
    """Build the cli."""
    parser = argparse.ArgumentParser(description='Bouillon')

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(function=_print_help)
    parser.set_defaults(check=True)
    parser.add_argument(
        '--dry-run', action='store_true', help='Perform a dry run.')
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICIAL'],
        default='WARNING', help='Set log level.')
    parser.add_argument(
        '--log-file', type=str, help='Set log file.')

    subparsers = parser.add_subparsers(help='Available sub commands')

    parser_setup = subparsers.add_parser(
        'setup',
        help='Setup installing dependencies, this will execute pip commands.')
    parser_setup.set_defaults(function=setup)

    parser_build = subparsers.add_parser('build', help='Build.')
    parser_build.set_defaults(function=build)

    parser_train = subparsers.add_parser('train', help='Train.')
    parser_train.set_defaults(function=train)

    parser_test = subparsers.add_parser('test', help='Run tests')
    parser_test.set_defaults(function=test)

    parser_test.add_argument(
        '--no-requirements', dest='requirements', action='store_false',
        help='Do not check installed modules against requirements files')

    parser_test.add_argument(
        '--no-vulnerabilities', dest='vulnerabilities', action='store_false',
        help='Do not check installed modules for security vulnerabilities.')

    parser_test.add_argument(
        '--no-pep8', dest='pep8', action='store_false',
        help='Do not check pep8 conformance.')

    parser_test.add_argument(
        '--no-static-check', dest='static', action='store_false',
        help='Do not perform static code analysis.')

    parser_test.add_argument(
        '--no-license-check', dest='licenses', action='store_false',
        help='Do not check that licenses of all used modules.')

    parser_test.add_argument(
        '--no-test-files-check', dest='test_files', action='store_false',
        help='Do not check that for each source file there is a test file.')

    parser_test.add_argument(
        '--no-unit-tests', dest='unit_tests', action='store_false',
        help='Do not run unit tests.')

    parser_test.add_argument(
        '--no-cicd-tests', dest='cicd_tests', action='store_false',
        help='Do not run CICD tests.')

    parser_upgrade = subparsers.add_parser(
        'upgrade',
        help='upgrade all dependencies (including bouillon).')
    parser_upgrade.set_defaults(function=upgrade)

    parser_clean = subparsers.add_parser('clean', help='Clean temp files.')
    parser_clean.set_defaults(function=clean)

    parser_release = subparsers.add_parser('release', help='release me.')
    parser_release.add_argument('version', type=str,
                                help='release version.')

    parser_release.set_defaults(function=release)

    return parser.parse_args()


def run_function(*, function: typing.Callable, **kwargs) -> None:
    """Run a step."""
    logger.debug(f'Running "{function.__name__}" step.')
    function(**kwargs)


def run_logging(*, log_level: str, log_file: str, **kwargs) -> None:
    """Do setup logging and run a step."""
    logging.basicConfig(filename=log_file, level=log_level)
    run_function(**kwargs)


if __name__ == '__main__':
    args = cli()

    # Unless we are running setup, make sure that bouillon was imported
    if args.function != setup and util.find_spec('bouillon') is None:
        logger.error('Failed to import bouillon, run "boil setup" first.')
        exit(1)

    run_logging(**vars(args))
