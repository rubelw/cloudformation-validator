#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import sys
from os import path
from io import open


DESCRIPTION = ("Lightweight, extensible schema and data validation tool for "
               "Cloudformation Templates.")

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


VERSION = '0.6.35'

setup_requires = (
    ['pytest-runner'] if any(x in sys.argv for x in ('pytest', 'test', 'ptr')) else []
)

setup(
    name='cloudformation_validator',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/rubelw/cloudformation-validator',
    author='Will Rubel',
    author_email='willrubel@gmail.com',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=setup_requires,
    tests_require=['pytest','mock'],
    test_suite="cloudformation_validator.tests",
    install_requires=[
        "boto3>=1.4.3",
        "requests>=2.18",
        "Click>=6.7",
        "PyYAML>=3.12",
        "pymongo>=3.4.0",
        "tabulate>=0.8",
        "configparser>=3.5.0",
        "jinja2>=2.10",
        "dill>=0.2.8",
        "pykwalify>=1.6.1",
        "schema>=0.6.8",
        "future>=0.16.0",
        "six>=1.11.0",
        "pip"
    ],
    keywords=['validation', 'schema', 'dictionaries','aws','cloudformation','python','rules','linter'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points="""
        [console_scripts]
        cfn-validator=cloudformation_validator.command:cli
    """
)