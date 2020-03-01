#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

import argparse
import glob
import importlib
import subprocess
import typing

optional_modules = ['bouillon']

for optional_module in optional_modules:
    try:
        module = importlib.import_module(optional_module)
    except:
        optional_modules.remove(optional_module)
    else:
        globals()[optional_module] = module


_repository_name = 'bouillion'

def _find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def _setup(**kwargs):
    """
    Setup the environment installing all dependencies in the requirement files.
    """
    for r in _find_requirement_files():
        print(f'# Installing dependencies from {r}')
        subprocess.run(f'pip install -r {r}', shell=True, check=True)


def _install(**kwargs):
    subprocess.run(f'pip install -e .', shell=True, check=True)


def _test(**kwargs):
    """
    Run tests
    """

    try:

        if kwargs["pep8"]:
            print('>> Checking pep8 conformance.')
            subprocess.run(
                'flake8 --per-file-ignores="__init__.py:F401"',
                shell=True,
                check=True,
            )

        if kwargs["static"]:
            print('>> Running static analysis check.')
            subprocess.run(
                'mypy **/*.py --config-file cicd/mypy.ini',
                shell=True,
                check=True
            )

        if kwargs["requirements"]:
            print('>> Checking installed dependencies versions.')
            for r in _find_requirement_files():
                subprocess.run(
                    f'requirementz --file {r}',
                    shell=True,
                    check=True
                )

        if kwargs["licenses"]:
            print('>> Checking license of dependencies.')
            for r in _find_requirement_files():
                subprocess.run(
                    f'liccheck -s cicd/licenses.ini -r {r}',
                    shell=True,
                    check=True
                )

        if kwargs["test_files"]:
            print('>> Checking for test files for all source files.')
            bouillon.check_test_files(
                glob.glob(f'src/{_repository_name}/**/*.py', recursive=True),
                glob.glob('test/src/**/test_*.py', recursive=True)
            )

        if kwargs["unittests"]:
            print('>> Running unittests.')
            subprocess.run(
                'pytest test/src --cov=bouillon --cov-fail-under=10 --durations=5 \
                -vv',
                shell=True,
                check=True
            )

        if kwargs["unittests"]:
            print('>> Running cicd tests.')
            subprocess.run(
                'pytest test/cicd --durations=5 -vv',
                shell=True,
                check=True
            )

    except subprocess.CalledProcessError as e:
        exit(e.returncode)


def _build(**kwargs):
    pass
    # raise Exception("build step not implemented")


def _release(**kwargs):
    raise Exception('relase step not implemented')


def _clean(**kwargs):
    raise Exception('Clean step not implemented')


def _upgrade(**kwargs):

    if kwargs['dependencies']:
        print('>> Updating module versions in requirement files.')

        for r in _find_requirements_files():
            subprocess.run(f"pur -r {r}", shell=True, check=True)

    if kwargs['bouillon']:
        print('>> Upgrading Bouillion version.')
        bouillon.upgrade_bouillion()


def cli():

    parser = argparse.ArgumentParser(description='Bouillon')

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(function=_print_help)
    subparsers = parser.add_subparsers(help='Sub commands')

    parser_setup = subparsers.add_parser('setup', help='Run setup.')
    parser_setup.set_defaults(function=_setup)

    parser_test = subparsers.add_parser('build', help='Run build')
    parser_test.set_defaults(function=_build)

    parser_test = subparsers.add_parser('install', help='Install')
    parser_test.set_defaults(function=_install)

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
        action='store_false',
    )

    parser_test.add_argument(
        '--no-static-check',
        dest='static',
        action='store_false',
    )

    parser_test.add_argument(
        '--no-license-check',
        dest='licenses',
        action='store_false',
    )

    parser_test.add_argument(
        '--no-test-files-check',
        dest='test_files',
        action='store_true',
    )

    parser_test.add_argument(
        '--no-unittests',
        dest='unittests',
        action='store_false',
    )

    parser_upgrade = subparsers.add_parser(
        'update', help='upgrade dependencies and bouillon.'
    )
    parser_upgrade.set_defaults(function=_upgrade)

    parser_upgrade.add_argument(
        '--no-dependencies',
        dest='dependencies',
        action='store_false',
        help='Do not update versions in requirement files.'
    )

    parser_upgrade.add_argument(
        '--no-bouillon',
        dest='bouillon',
        action='store_false',
        help='Do not update bouillon.'
    )

    parser_release = subparsers.add_parser('release', help='release me.')
    parser_release.set_defaults(function=_release)

    return parser.parse_args()


if __name__ == '__main__':
    args = cli()

    if args.function != _setup:
        for f in optional_modules:
            print(f'Failed importing {f}, run "boil setup" first.')

    args.function(**vars(args))
