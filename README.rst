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
paced python projects.

Bouillon contains; a) a project structure, b) a Command Line Interface (CLI)
for releasing etc., that is easy to adapt and, c) a module that
provides helper functionality when writing your cli.

The idea is that you together with your project ship a program that assist the
developers to release the project, and other tedious tasks, helping you to;

* Reduce time spent on repetetive tasks.
* Guareentee a well defined development environement, reducing human error.
* Simplify setup of CI/CD, as the same commands locally and remotely.


Getting Started
---------------

::

    git clone git@github.com:janusheide/bouillon.git
    cd bouillon

    python boil.py --help

Will pip install packages (a venv is recommended)::

    pip install .[dev]
    python boil.py --help
    python boil.py release 0.0.1


Settings
--------

The following settings can be overwritten in ``pyproject.toml``::

    [tool.bouillon]
    news_files = ["NEWS.rst",]
    distribution_dirs = ["dist",]
    build_steps = [["python", "-m", "build"],]
    lint_steps = [["brundle"],]
    test_steps = [["pytest"],]



Start A New Project
...................

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

    ├── boil.py (modify)
    ├── LICENSE.txt (replace)
    ├── NEWS.rst (replace)
    ├── pyproject.toml (modify)
    ├── README.rst (replace)
    ├── src (replace)
    │   ├── bouillon
    │   │   ├── bouillon.py
    │   │   ├── git.py
    │   │   └── __init__.py
    └── test (replace)
        ├── bouillon
        │   ├── test_bouillon.py
        │   └── test_git.py
        └── test_boil.py

At some point it might be convenient to fork *this* repository, make any changes
you need and use that as your template repository.


Logging
-------

Supports standard log levels; ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``, and writing
log to a file.

Set the log level to ``DEBUG``::

    python boil --log-level=DEBUG test

Set the log level to ``DEBUG`` and redirect output from executed commands to
``bar.log``::

    python boil --log-level=DEBUG test >> bar.log

Set the log level to ``DEBUG`` and redirect output from executed commands to
``bar.log`` and log information to ``foo.log``::

    python boil --log-level=DEBUG --log-file=foo.log test >> bar.log

Set the log level to ``DEBUG`` and redirect output from executed commands and
log information to ``foo.log``::

    python boil --log-level=DEBUG --log-file=foo.log test >> foo.log


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
* The master should always be green.

Simplicity
..........

* Simplicity over features.
* Components should be easy to replace.

Automation
..........

* Reduce maintenance, repetitive tasks, and human errors.
* Easy to upgrade dependencies.
* Use merge policies and triggered and scheduled events.
