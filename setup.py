#! /usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2020, Janus Heide.
# All rights reserved.
#
# Distributed under the "BSD 3-Clause License", see LICENSE.txt.

import io

from setuptools import setup, find_packages

with io.open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='bouillon',
    use_scm_version=True,
    description=("Tool for managing machine learning model and service "
                 "projects and other fast paced python projects."),
    license='BSD-3-Clause',
    long_description=long_description,
    url='https://github.com/janusheide/bouillon',
    author='Janus Heide',
    author_email='janusheide@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    entry_points={
        'console_scripts': ['boil=boil.__main__:run'],
    },
    keywords=['building', 'maintenance', 'utility'],
    packages=find_packages(where='src', exclude=['test']),
    package_dir={"": "src"},
    python_requires='>=3.7',
    install_requires=[''],
    setup_requires=['setuptools_scm'],
)
