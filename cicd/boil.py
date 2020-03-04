#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.

import argparse
import glob
from importlib import util
import os
import typing

# import bouillon if found, ebables running setup without bouillon.
bouillon_loader = util.find_spec('bouillon')
if bouillon_loader is not None:
    import bouillon


_repository = 'bouillon'


def _find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def _setup(**kwargs):

    for r in _find_requirement_files():
        bouillon.run([f'pip install -r {r}'], **kwargs)


def _test(pep8: bool, static: bool, requirements: bool, licenses: bool,
          test_files: bool, unittests: bool, **kwargs) -> None:

    if pep8:
        bouillon.run([f'flake8'], **kwargs)

    if static:
        bouillon.run(['mypy', 'src/**/*.py', '--config-file cicd/mypy.ini'],
                     **kwargs)

    if requirements:
        for r in _find_requirement_files():
            bouillon.run([f'requirementz', f'--file {r}'], **kwargs)

    if licenses:
        for r in _find_requirement_files():
            bouillon.run(
                [f'liccheck', '-s cicd/licenses.ini', f'-r {r}'], **kwargs)

    if test_files:
        if not bouillon.check_for_test_files(os.path.join('src', _repository),
                                             os.path.join('test', 'src')):
            exit(1)

    if unittests:
        bouillon.run(
            ['pytest', os.path.join('test', 'src'), '--cov=bouillon',
                '--cov-fail-under=10', '--durations=5', '-vv'],
            **kwargs)

    if unittests:
        bouillon.run(
            ['pytest', os.path.join('test/cicd'), '--durations=5', '-vv'],
            **kwargs)


def _build(**kwargs):

    bouillon.run('python setup.py sdist', **kwargs)
    bouillon.run('python setup.py bdist_wheel --universal', **kwargs)


def _train(**kwargs):
    raise Exception("train step not implemented")


def _upgrade(upgrade_dependencies: bool, upgrade_bouillon: bool, **kwargs):

    if upgrade_dependencies:
        for r in _find_requirement_files():
            bouillon.run([f'pur -r {r}', '--skip bouillon'], **kwargs)

    if upgrade_bouillon:
        bouillon.run(
            [f'pur -r cicd/requirements.txt', '--only bouillon'], **kwargs)


def _release(**kwargs):

    _upgrade(upgrade_dependencies=True, upgrade_bouillon=True)

    _test(pep8=True, static=True, requirements=True, licenses=True,
          test_files=True, unittests=True)

    _build()

    raise Exception('release step not implemented')
    # Todo upload it to pip


def _clean(**kwargs):
    raise Exception('Clean step not implemented')


def cli():

    parser = argparse.ArgumentParser(description='Bouillon')

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(function=_print_help)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--silent', action='store_true')
    parser.add_argument('--verbose', action='store_true')

    subparsers = parser.add_subparsers(help='Sub commands')

    parser_setup = subparsers.add_parser('setup', help='Run setup step.')
    parser_setup.set_defaults(function=_setup)

    parser_build = subparsers.add_parser('build', help='Run build step.')
    parser_build.set_defaults(function=_build)

    parser_train = subparsers.add_parser('train', help='Run train step.')
    parser_train.set_defaults(function=_train)

    parser_test = subparsers.add_parser('test', help='Run tests')
    parser_test.set_defaults(function=_test)

    parser_test.add_argument(
        '--no-requirements',
        dest='requirements',
        action='store_false',
    )

    parser_test.add_argument(
        '--no-pep8-check',
        dest='pep8',
        action='store_false')

    parser_test.add_argument(
        '--no-static-check',
        dest='static',
        action='store_false')

    parser_test.add_argument(
        '--no-license-check',
        dest='licenses',
        action='store_false')

    parser_test.add_argument(
        '--no-test-files-check',
        dest='test_files',
        action='store_false')

    parser_test.add_argument(
        '--no-unittests',
        dest='unittests',
        action='store_false')

    parser_upgrade = subparsers.add_parser(
        'upgrade', help='upgrade dependencies and bouillon.')
    parser_upgrade.set_defaults(function=_upgrade)

    parser_upgrade.add_argument(
        '--no-dependencies',
        dest='upgrade_dependencies',
        action='store_false',
        help='Do not upgrade versions in requirement files.')

    parser_upgrade.add_argument(
        '--no-bouillon',
        dest='upgrade_bouillon',
        action='store_false',
        help='Do not upgrade bouillon.')

    parser_release = subparsers.add_parser('release', help='release me.')
    parser_release.set_defaults(function=_release)

    return parser.parse_args()


if __name__ == '__main__':
    args = cli()

    # Unless we are running setup, make sure that bouillon was imported
    if args.function != _setup and bouillon_loader is None:
        print(f'Failed to import bouillon, run "boil setup" first.')
        exit(1)

    args.function(**vars(args))
