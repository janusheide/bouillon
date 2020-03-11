..  Copyright (c) Janus Heide 2020.
..  All rights reserved.

Bouillon
========

Bouillon contains; a) a project structure, b) a script for building, testing, 
etc., that are easy to adapt and, c) a module that provides helper 
functionality when writing your script.

The use is intended, but not limited to, projecs with frequently releases, e.g. 
ML models and services. 
The goal is to make it quick and easy to set up a new project with the basic testing and releasing functionality.


User Friendly
.............

The example script is plain Python with the intension of using modules that 
many will already be familiar with.

Reproduceability
................


All dependcies shoud be hard (versioned)

This 



Simplicity
..........

Since the 



Automation
..........

Mininize the maintaince burden

Easy to upgrade dependencies




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



Pip Dependency
..............

Since the version is defined in cicd/requirements.txt 


Copy Module Source
..................


Avoid Using Module
..................


Copy Module Source Into Script
..............................
