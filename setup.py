#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) Janus Heide 2020.
# All rights reserved.


import io

from setuptools import setup, find_packages

with io.open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='bouillon',
    use_scm_version=True,
    description=("Tool for managing machine learning model and service"
                 "projects and other fast pased python projects."),
    long_description=long_description,
    url='https://github.com/janusheide/bouillion',
    author='Janus Heide',
    author_email='janusheide@gmail.com',
    license='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License ::',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    entry_points={
        'console_scripts': ['boil=boil.__main__:run'],
    },
    keywords=('building', 'maintaince', 'utility'),
    packages=find_packages(where='src', exclude=['test']),
    package_dir={"": "src"},
    install_requires=[''],
)
