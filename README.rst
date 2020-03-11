..  Copyright (c) Janus Heide 2020.
..  All rights reserved.

Bouillon
========

.. image:: https://github.com/janusheide/bouillon/workflows/Unit%20tests/badge.svg
    :target: https://github.com/janusheide/bouillon/commits/master
    :alt: Unit tests
 
Bouillon contains; a) a project structure, b) a script for building, testing, 
etc., that are easy to adapt and, c) a module that provides helper 
functionality when writing your script.

Features
--------

The script provides various usful functionality using various projects, e.g.:

* Pep8 syntax enforcement.
* Static Code Analysis.
* Verfifcation of installed dependencies against refined dequirements.
* Verfification of licenses in included modules.
* Execution of unit tests.
* Converage of unit tests.
* API documentation.
* Updating of dependencies.

Objectives
----------

The use is intended, but not limited to, projecs with frequently releases, e.g. 
ML models and services. 
The goal is to make it quick and easy to set up a new project with the basic testing and releasing functionality.

User Friendly
.............

The example script is plain Python with the intension of using modules that 
many will already be familiar with.

Should be convininent to setup and run both locally and remotely

Reproduceability
................

The master should always be green, stable point to work from.
Depends on merge policies which should be setup in your repository of choice.

All dependcies shoud be hard (versioned).


Simplicity
..........

Prefer simpler options to make it easier for more users.

Essentially a bunch of small buildingin blocks, ensure that components can be exchanged quickly.


Automation
..........

Mininize the maintaince burden by 

Easy to upgrade dependencies

This is primarily 

Setup triggerede and scheduled actions 

periodic try to update



Getting Started
---------------


::

    git clone git@github.com:janusheide/bouillon.git
    cd bouillon 

    python boul --help

    python boil setup (will pip install packages, so a venv is recommended)
    python boil test



Start A New Project
...................

You can use this repository as a template

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template


Alternatively a more manual approach could be something like the following, 
where new_project is a empty git repository.

::

    (clone the repository and remove the history)
    git clone git@github.com:janusheide/bouillon.git
    cd bouillon
    rm -rf .git
    
    (copy the project structure into your existing (empty) git repository)
    cp -r * ../new_project
    cd ../new_project/
    git add .
    git commit -m 'Initial commit'
    git push


You should now have a project with the following structure, and should modify 
as indicated below.

::

    ├── README.rst (replace)
    ├── boil -> cicd/boil.py
    ├── cicd
    │   ├── boil.py (modify commands as needed)
    │   ├── licenses.ini (verify acceptable licenses)
    │   ├── mypy.ini
    │   └── requirements.txt
    ├── examples
    ├── setup.py (modify)
    ├── src
    │   ├── bouillon (modify or replace files with you implementation)
    │   │   ├── __init__.py
    │   │   ├── bouillon.py
    │   │   └── requirements.txt
    └── test
        ├── cicd
        │   └── test_boil_cli.py (modify to reflect your commands)
        ├── requirements.txt
        └── src (replace with your tests)
            ├── test___init__.py
            └── test_bouillon.py


At some point it might be convininent to fork the reposiotry, make any changes 
you need and use that as your template reposiotry.


Ways of Inclusion
-----------------

You can include the bouillon module in a number of ways in your script, below
are some prioritized options.


Pip Install During Setup Step
.............................

Install the module using Pip. This requires that the initial setup step can be 
executed without importing the module. 


Pip Install Prior to Executing Script
.....................................

The module can be installed prior to running any script commands, but this 
requires an extra step and means that the script setup step only partly setup 
the environment.


Copy Module Source
..................

Copy the module implementation (bouillon.py) into your project and import it 
from the local file in your script. Consequently you will have to manually 
update the module or implement a way to push a new module version into multiple 
repositories.


Copy Module Source Into Script
..............................

Copy the module implementation or the fnuctionality you need into your script. 
While it is simple but even more inconvinient to keep the module functionality 
up to date.
