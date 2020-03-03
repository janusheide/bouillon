#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright Janue Heide 2020

import argparse
import glob
from importlib import util
import os
import typing

# import bouillon if found, ebables running setup without bouillon.
bouillon_loader = util.find_spec('bouillon')
if bouillon_loader is not None:
    import bouillon


_repository_name = 'bouillon'


def _find_requirement_files() -> typing.List[str]:
    return glob.glob('**/*requirements.txt', recursive=True)


def _setup(**kwargs):
    """
    Setup the environment installing all dependencies in the requirement files.
    """
    for r in _find_requirement_files():
        print(f'>> Installing dependencies from {r}')
        bouillon.run([f'pip install -r {r}'], **kwargs)


def _test(pep8: bool, static: bool, requirements: bool, licenses: bool,
          test_files: bool, unittests: bool, **kwargs) -> None:
    """
    Run tests
    """

    if pep8:
        print('>> Checking pep8 conformance.')
        bouillon.run(
            [f'flake8'], **kwargs)

    if static:
        print('>> Running static analysis check.')
        bouillon.run(['mypy **/*.py', '--config-file cicd/mypy.ini'], **kwargs)

    if requirements:
        print('>> Checking installed dependencies versions.')
        for r in _find_requirement_files():
            bouillon.run([f'requirementz --file {r}'], **kwargs)

    if licenses:
        print('>> Checking license of dependencies.')
        for r in _find_requirement_files():
            bouillon.run([f'liccheck -s cicd/licenses.ini -r {r}'], **kwargs)

    if test_files:
        print('>> Checking for test files for all source files.')
        bouillon.check_for_test_files(
            glob.glob(os.path.join('src', _repository_name, '**', '*.py'),
                      recursive=True),
            glob.glob(os.path.join('test/src/**', 'test_*.py'), recursive=True)
        )

    if unittests:
        print('>> Running unittests.')
        bouillon.run([
            'pytest', os.path.join('test', 'src'), '--cov=bouillon',
            '--cov-fail-under=10', '--durations=5', '-vv'], **kwargs)

    if unittests:
        print('>> Running cicd tests.')
        bouillon.run(['pytest', os.path.join('test/cicd'),
                     '--durations=5', '-vv'], **kwargs)


def _build(**kwargs):
    pass
    # raise Exception("build step not implemented")


def _release(**kwargs):
    raise Exception('relase step not implemented')


def _clean(**kwargs):
    raise Exception('Clean step not implemented')


def _upgrade(upgrade_dependencies: bool, upgrade_bouillon: bool, **kwargs):

    if upgrade_dependencies:
        print('>> Updating module versions in requirement files.')
        for r in _find_requirement_files():
            bouillon.run([f'pur -r {r}', '--skip bouillon'], **kwargs)

    if upgrade_bouillon:
        print('>> Upgrading Bouillion version.')
        bouillon.run(
            [f'pur -r cicd/requirements.txt', '--only bouillon'], **kwargs)


def cli():

    parser = argparse.ArgumentParser(description='Bouillon')

    def _print_help(**kwargs):
        parser.print_help()

    parser.set_defaults(function=_print_help)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--silent', action='store_true')
    parser.add_argument('--verbose', action='store_true')

    subparsers = parser.add_subparsers(help='Sub commands')

    parser_setup = subparsers.add_parser('setup', help='Run setup.')
    parser_setup.set_defaults(function=_setup)

    parser_test = subparsers.add_parser('build', help='Run build')
    parser_test.set_defaults(function=_build)

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
        'upgrade', help='upgrade dependencies and bouillon.'
    )
    parser_upgrade.set_defaults(function=_upgrade)

    parser_upgrade.add_argument(
        '--no-dependencies',
        dest='upgrade_dependencies',
        action='store_false',
        help='Do not upgrade versions in requirement files.'
    )

    parser_upgrade.add_argument(
        '--no-bouillon',
        dest='upgrade_bouillon',
        action='store_false',
        help='Do not upgrade bouillon.'
    )

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
