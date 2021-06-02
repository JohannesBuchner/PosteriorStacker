#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except:
    from distutils.core import setup

try:
    with open('README.rst') as readme_file:
        readme = readme_file.read()

    with open('HISTORY.rst') as history_file:
        history = history_file.read()
except IOError:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
        readme = readme_file.read()

    with open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')) as history_file:
        history = history_file.read()

requirements = ['numpy', 'scipy', 'ultranest', 'matplotlib', 'pandas']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Johannes Buchner",
    author_email='johannes.buchner.acad@gmx.com',
    python_requires='>=3.5.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Combine Bayesian analyses from many datasets. Easy sample parameter distributions.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    keywords='posteriorstacker',
    name='posteriorstacker',
    scripts=['posteriorstacker.py', 'load_ultranest_outputs.py'],
    #py_modules=['posteriorstacker'],
    setup_requires=setup_requirements,
    #test_suite='tests',
    #tests_require=test_requirements,
    url='https://github.com/JohannesBuchner/PosteriorStacker',
    version='0.6.1',
)
