#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import sys


DESCRIPTION = ("Lightweight, extensible schema and data validation tool for "
               "Cloudformation Templates.")
LONG_DESCRIPTION = open('README.rst').read()
VERSION = '0.2.29'

setup_requires = (
    ['pytest-runner'] if any(x in sys.argv for x in ('pytest', 'test', 'ptr', 'future')) else []
)



setup(
    name='cloudformation_validator',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/rubelw/cloudformation-validator',
    author='Will Rubel',
    author_email='willrubel@gmail.com',
    long_description=LONG_DESCRIPTION,
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=setup_requires,
    package_data={'cfn_model': ['schema/*.json','schema/*.yml','schema/*.erb']},
    tests_require=['pytest'],
    test_suite="cloudformation_validator.tests",
    install_requires=[
        "boto3>=1.4.3",
        "requests>=2.18",
        "Click>=6.7",
        "PyYAML>=3.12",
        "pymongo>=3.4.0",
        "tabulate>=0.8",
        "configparser",
        "jinja2",
        "dill",
        "pykwalify",
        "schema"
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