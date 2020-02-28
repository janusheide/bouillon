#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue heide 2020

import argparse
import subprocess

import bouillon


def _setup(**kwargs):
    """
    Setup the environment installing all dependencies in the requirement files.
    """
    for r in bouillon.find_requirements_files():
        print(f'# Installing dependencies from {r}')
        subprocess.run(f'pip install -r {r}', shell=True, check=True)


def _install(**kwargs):
    subprocess.run(f'pip install -e .', shell=True, check=True)


def _test(**kwargs):
    """
    Run tests
    """

    try:

        if kwargs["requirements"]:
            print('>> Checking installed dependencies versions.')
            bouillon.check_environment_modules(
                bouillon.find_requirements_files()
            )

        if kwargs["licenses"]:
            print('>> Checking license of dependencies.')
            bouillon.check_module_licenses(
                bouillon.find_requirements_files()
            )

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

        if kwargs["test_files"]:
            print('>> Checking for test files for all source files.')
            bouillon.check_test_files("src/", "test/src/")

        if kwargs["unittests"]:
            print('>> Running unittests.')
            subprocess.run(
                'pytest test --cov-fail-under=100 --durations=5 -vv',
                shell=True,
                check=True
            )

    except subprocess.CalledProcessError as e:
        exit(e.returncode)


def _build(**kwargs):
    raise Exception("build step not implemented")


def _release(**kwargs):
    raise Exception('relase step not implemented')


def _clean(**kwargs):
    raise Exception('Clean step not implemented')


def _upgrade(**kwargs):

    if kwargs['dependencies']:
        print('>> Updating module versions in requirement files.')
        bouillon.update_requirements_files(
            bouillon.find_requirements_files()
        )

    if kwargs['bouillon']:
        raise Exception('Upgrade of bouillon not implemented')


def cli():

    parser = argparse.ArgumentParser(description='Bouillon')

    def print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(func=print_help)
    subparsers = parser.add_subparsers(help='Sub commands')

    parser_setup = subparsers.add_parser('setup', help='Run setup.')
    parser_setup.set_defaults(func=_setup)

    parser_test = subparsers.add_parser('build', help='Run build')
    parser_test.set_defaults(func=_build)

    parser_test = subparsers.add_parser('install', help='Install')
    parser_test.set_defaults(func=_install)

    parser_test = subparsers.add_parser('test', help='Run tests')
    parser_test.set_defaults(func=_test)

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
    parser_upgrade.set_defaults(func=_upgrade)

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
    parser_release.set_defaults(func=_release)

    return parser.parse_args()


if __name__ == '__main__':

    print("bouil")
    args = cli()

    args.func(**vars(args))
