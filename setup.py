#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'pyserial', 'enum-compat', 'pexpect']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Jonathan William Morley",
    author_email='jon@robowunderkind.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7'
       
    ],
    description="Robo Wunderkind Python API - BLED112 USB Dongle Required",
    entry_points={
        'console_scripts': [
            'robopython=robopython.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='robopython',
    name='robopython',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JonRobo/robopython',
    version='0.4.5',
    zip_safe=False,
)
