#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.

import argparse
import glob
from importlib import util
import os
import subprocess
import typing

# import bouillon if found, ebables running setup without bouillon.
bouillon_loader = util.find_spec('bouillon')
if bouillon_loader is not None:
    import bouillon


def _find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def _setup(*, dry_run, verbose, **kwargs):

    if dry_run or verbose:
        print('Installing dependencies')

    if dry_run:
        exit(0)

    # Install the local project, for your project add bouillon to requirements
    subprocess.run(['pip', 'install', '-e', '.'], **kwargs)

    for r in _find_requirement_files():
        subprocess.run([f'pip', 'install', '-r', f'{r}'], **kwargs)


def _test(*, pep8: bool, static: bool, requirements: bool, licenses: bool,
          test_files: bool, unit_tests: bool, cicd_tests: bool,
          **kwargs) -> None:

    if pep8:
        bouillon.run([f'flake8'], **kwargs)

    if static:
        bouillon.run(['mypy', 'src', f'--config-file', 'cicd/mypy.ini'],
                     **kwargs)

    # https://pypi.org/project/Requirementz/
    if requirements:
        for r in _find_requirement_files():
            bouillon.run([f'requirementz', f'--file', f'{r}'], **kwargs)

    # https://github.com/dhatim/python-license-check
    if licenses:
        for r in _find_requirement_files():
            bouillon.run([f'liccheck', f'-s', f'cicd/licenses.ini',
                          f'-r', f'{r}'], **kwargs)

    if test_files:
        if not bouillon.check_for_test_files(
            os.path.join('src', bouillon.git_repository_name()),
                os.path.join('test', 'src')):
            exit(1)

    if unit_tests:
        bouillon.run(
            [f'pytest', f'{os.path.join("test", "src")}', '--cov=bouillon',
                '--cov-fail-under=90', '--durations=5', '-vv'], **kwargs)

    if cicd_tests:
        bouillon.run([f'pytest', f'{os.path.join("test", "cicd")}',
                      '--durations=5', '-vv'], **kwargs)


def _build(**kwargs):

    bouillon.run(['python setup.py sdist'], **kwargs)
    bouillon.run(['python setup.py bdist_wheel --universal'], **kwargs)


def _train(**kwargs):
    raise Exception("train step not implemented")


def _upgrade(**kwargs):

    # https://github.com/alanhamlett/pip-update-requirements
    for r in _find_requirement_files():
        bouillon.run([f'pur', '-r', f'{r}', '--force'], **kwargs)


def _release(*, version, **kwargs):

    print(f'Releasing with version {version}')
    print(f'Current git commit id is {bouillon.git_commit_id()}')
    print(f'Current tags {bouillon.git_tags()}')
    return(0)

    _upgrade(**kwargs)

    _test(pep8=True, static=True, requirements=True, licenses=True,
          test_files=True, unit_tests=True, cicd_tests=True, **kwargs)

    _build(**kwargs)

    # raise Exception('release step not implemented')
    # Todo upload it to pip


def _clean(**kwargs):
    raise Exception('Clean step not implemented')


def cli():

    parser = argparse.ArgumentParser(description='Bouillon')

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(function=_print_help)
    parser.set_defaults(check=True)
    parser.add_argument(
        '--dry-run', action='store_true', help='Perform a dry run.')
    parser.add_argument(
        '--verbose', action='store_true', help='More verbose printing')

    subparsers = parser.add_subparsers(help='Available sub commands')

    parser_setup = subparsers.add_parser(
        'setup',
        help='Setup installing dependencies, this will execute pip commands.')
    parser_setup.set_defaults(function=_setup)

    parser_build = subparsers.add_parser('build', help='Build.')
    parser_build.set_defaults(function=_build)

    parser_train = subparsers.add_parser('train', help='Train.')
    parser_train.set_defaults(function=_train)

    parser_test = subparsers.add_parser('test', help='Run tests')
    parser_test.set_defaults(function=_test)

    parser_test.add_argument(
        '--no-requirements', dest='requirements', action='store_false',
        help='Do not check installed modules against requirements files')

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
        help='Do not check that for each source file there is a test file')

    parser_test.add_argument(
        '--no-unit-tests', dest='unit_tests', action='store_false',
        help='Do not run unit tests.')

    parser_test.add_argument(
        '--no-cicd-tests', dest='cicd_tests', action='store_false',
        help='Do not run CICD tests.')

    parser_upgrade = subparsers.add_parser(
        'upgrade',
        help='upgrade all dependencies (including bouillon).')
    parser_upgrade.set_defaults(function=_upgrade)

    parser_release = subparsers.add_parser('release', help='release me.')
    parser_release.add_argument('--version', type=str,
                                help='release version.')

    parser_release.set_defaults(function=_release)

    return parser.parse_args()


def _call(*, function, **kwargs):
    function(**kwargs)


if __name__ == '__main__':
    args = cli()

    # Unless we are running setup, make sure that bouillon was imported
    if args.function != _setup and bouillon_loader is None:
        print(f'Failed to import bouillon, run "boil setup" first.')
        exit(1)

    _call(**vars(args))
