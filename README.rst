..  Copyright (c) 2020, Janus Heide.
..  All rights reserved.
..
.. Distributed under the "BSD 3-Clause License", see LICENSE.rst.

Bouillon
========

.. image:: https://github.com/janusheide/bouillon/actions/workflows/unittests.yml/badge.svg
    :target: https://github.com/janusheide/bouillon/actions/workflows/unittests.yml
    :alt: Unit tests

.. image:: https://img.shields.io/pypi/pyversions/bouillon
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/librariesio/github/janusheide/bouillon
   :alt: Libraries.io dependency status for GitHub repo

A Tool for releasing machine learning model and service projects and other fast
paced python projects. The base module can also be used as a basis for a custom
cli.

Bouillon contains; a) a project structure, b) a Command Line Interface (CLI)
for releasing etc., that is easy to adapt and, c) a couple of modules that
provides helper functionality if your writing your own cli.

The idea is that you together with your project ship a program that assist the
developers to release the project, and other tedious tasks, helping you to;

* Reduce time spent on repetetive tasks.
* Guareentee a well defined development environement, reducing human error.
* Simplify setup of CI/CD, as the same commands locally and remotely.


Getting Started
---------------

Will pip install packages (a venv is recommended)::

    pip install bouillon[standard]
    bouillon --help
    bouillon release 0.0.1

Print help for the ``release`` command::

    bouillon release --help
    usage: bouillon release [-h]
                            [--check_clean_branch]
                            [--releaseable_branch RELEASEABLE_BRANCH]
                            [--distribution_dir DISTRIBUTION_DIR]
                            [--news_files NEWS_FILES]
                            [--build_steps BUILD_STEPS]
                            [--lint_steps LINT_STEPS]
                            [--test_steps TEST_STEPS]
                            version

    The following checks and actions will be performed:

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

    positional arguments:
    version               release version (e.g. '1.2.3').

    options:
    -h, --help            show this help message and exit
    --check_clean_branch  Check that the current branch is clean. (default: True)
    --releaseable_branch RELEASEABLE_BRANCH
                            Branches from which release is allowed ('*' for any branch) (default: main)
    --distribution_dir DISTRIBUTION_DIR
                            Distribution directory. (default: dist)
    --news_files NEWS_FILES
                            News files to open for edits. (default: ['NEWS.rst'])
    --build_steps BUILD_STEPS
                            List of build steps. (default: [['python', '-m', 'build']])
    --lint_steps LINT_STEPS
                            List of lint steps. (default: [['brundle']])
    --test_steps TEST_STEPS
                            List of test steps. (default: [['pytest']])


.. note::

    If the upload to pypi fails for any reason the tag will be deleted and the
    release commit will be rolled back.


Settings
--------

The following settings (with defaults) can be overwritten in ``pyproject.toml``::

    [tool.bouillon]
    check_clean_branch = true
    releaseable_branch = the git default branch
    distribution_dir = "dist"
    news_files = ["NEWS.rst",]
    build_steps = [["python", "-m", "build"],]
    lint_steps = [["brundle"],]
    test_steps = [["pytest"],]


.. note::

    releaseable_branch defaults to the git default branch, but can be set to a
    static branch name like "dev" or "*" if all branches are permitted.


Logging
-------

Supports standard log levels; ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``, and writing
log to a file.

Set the log level to ``DEBUG``::

    bouillon --log-level=DEBUG test

Set the log level to ``DEBUG`` and redirect output from executed commands to
``bar.log``::

    bouillon --log-level=DEBUG test >> bar.log

Set the log level to ``DEBUG`` and redirect output from executed commands to
``bar.log`` and log information to ``foo.log``::

    bouillon --log-level=DEBUG --log-file=foo.log test >> bar.log

Set the log level to ``DEBUG`` and redirect output from executed commands and
log information to ``foo.log``::

    bouillon --log-level=DEBUG --log-file=foo.log test >> foo.log


Customize CLI
-------------

The standard bouillon command relies on varios other tools, e.g. pytest, twine
and various linters, if you want to use some other tools you can install the
base dependencies only, install the tools you like and configure bouillon
according or make you own cli altogheter.::

    pip install bouillon

You can get the base cli by downloading this git repository, e.g.::

    git clone git@github.com:janusheide/bouillon.git
    cd src/bouillon


Start A New Project
-------------------

You can use *this* repository as a template, `use repository as a template guide. <https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template>`__


Alternatively a more manual approach could be something like the following,
where new_project is a empty git repository.

Clone the repository and remove the history::

    git clone git@github.com:janusheide/bouillon.git
    cd bouillon
    rm -rf .git

Copy the project structure into your existing (empty) git repository::

    cp -r * ../new_project
    cd ../new_project/
    git add .
    git commit -m 'Initial commit'
    git push


You should now have a project with the following structure, and should modify
as indicated below::

    ├── LICENSE.txt (replace)
    ├── NEWS.rst (replace)
    ├── pyproject.toml (modify)
    ├── README.rst (replace)
    ├── src (replace)
    │   ├── bouillon
    │   │   ├── bouillon.py
    │   │   ├── cli.py (optinally copy and modify)
    │   │   ├── git.py
    │   │   └── __init__.py
    └── test (replace)
        └── bouillon
            ├── test_bouillon.py
            ├── test_cli.py
            └── test_git.py

At some point it might be convenient to fork *this* repository, make any changes
you need and use that as your template repository.


Goals
-----

The primary use is intended for, but not limited to, projects with frequently
releases, e.g. ML models and services.
The goal is to make it quick and easy to set up a new project with the basic
testing and releasing functionality.

User Friendliness
.................

* Make the life of the user easier.
* Use plain Python and modules that many are familiar with.
* Quick and easy to setup and run repetitive tasks.
* All tasks should be equally easy to rin locally as in a CI/CD environement.

Reproducibility
................

* Results and builds should be easy to reproduce.
* All dependencies must be hard (versioned).
* The main branch should always be green.

Simplicity
..........

* Simplicity over features.
* Components should be easy to replace.

Automation
..........

* Reduce maintenance, repetitive tasks, and human errors.
* Easy to upgrade dependencies.
* Use merge policies and triggered and scheduled events.
