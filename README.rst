..  Copyright (c) 2020, Janus Heide.
..  All rights reserved.
.. 
.. Distributed under the "BSD 3-Clause License", see LICENSE.rst.


Bouillon
========

.. image:: https://github.com/janusheide/bouillon/workflows/Unit%20tests/badge.svg?branch=master
    :target: https://github.com/janusheide/bouillon/commits/master
    :alt: Unit tests
 
Bouillon contains; a) a project structure, b) a Command Line Interface (CLI) 
for building, testing, etc., that are easy to adapt and, c) a module that 
provides helper functionality when writing your cli.

The idea is that you together with your project ship a program that assist the
developers to setup a development environment, run tests, release the project,
and other tedious tasks, helping you to;

* Reduce time spent on repetetive tasks.
* Guareentee a well defined development environement, reducing human error.
* Simplify setup of CI/CD, as the same commands locally and remotely.


Features
--------

The cli provides various useful functionality using various projects, e.g.:

* Pep8 syntax enforcement.
* Static Code Analysis.
* Verification of installed dependencies against requirements.
* Verification of licenses in included modules.
* Execution of unit tests.
* Coverage of unit tests.
* API documentation.
* Updating of dependencies.


Getting Started
---------------

::

    git clone git@github.com:janusheide/bouillon.git
    cd bouillon 

    python boil --help

Will pip install packages, a venv is recommended::

    python boil setup 
    python boil test

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

    ├── boil -> cicd/boil.py
    ├── cicd (modify)
    │   ├── boil.py
    │   ├── licenses.ini
    │   ├── mypy.ini
    │   └── requirements.txt
    ├── LICENSE.txt (replace)
    ├── NEWS.rst (replace)
    ├── README.rst (replace)
    ├── setup.py (modify)
    ├── src (replace)
    │   ├── bouillon
    │   │   ├── bouillon.py
    │   │   ├── __init__.py
    │   │   └── requirements.txt
    └── test (replace)
        ├── cicd
        │   └── test_boil_cli.py
        ├── requirements.txt
        └── src
            ├── test_bouillon.py
            └── test___init__.py



At some point it might be convenient to fork *this* repository, make any changes 
you need and use that as your template repository.


Ways of Inclusion
-----------------

You can include the bouillon module in a number of ways in your script, below
are some options prioritized options.


Pip Install During Setup Step
.............................

Install the module using Pip. This requires that the initial setup step can be 
executed without importing the module. 


Pip Install Prior to Executing Script
.....................................

Install the module prior to running any script commands, this adds an extra 
step and consequently the script *setup step* only partly setup the environment.

Copy Module File
..................

Copy the module implementation (bouillon.py) into your project and import it 
from the local file in your script. Consequently you will have to manually 
update the module or implement a way to push a new module version into your 
repository.

Copy Module Source Into CLI file
................................

Copy the module implementation or the functionality you need into your cli file. 
While it is simple but even more inconvenient to keep the module functionality 
up to date.


Logging
-------

Supports standard log levels; DEBUG, INFO, WARING, ERROR, CRITICAL, and writing 
log to a file.

Set the log level to ``debug``::

    python boil --log-level=DEBUG test

Set the log level to ``debug`` and redirect output from executed commands to
``bar.log``::

    python boil --log-level=DEBUG test >> bar.log

Set the log level to ``debug`` and redirect output from executed commands to
``bar.log`` and log information to ``foo.log``::

    python boil --log-level=DEBUG --log-file=foo.log test >> bar.log

Set the log level to ``debug`` and redirect output from executed commands and
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
    