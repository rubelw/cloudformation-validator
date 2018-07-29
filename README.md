cloudformation\_validator
=========================

Features
--------

cloudformation\_validator provides type checking and other base
functionality out of the box and is designed to be non-blocking and
easily extensible, allowing for custom validation. It has no
dependencies and is thoroughly tested under Python 2.7, Python 3.3,
Python 3.4, Python 3.5, Python 3.6.

Funding
-------

cloudformation\_validator is a open source, collaboratively funded
project. If you run a business and are using cloudformation\_validator
in a revenue-generating product, it would make business sense to sponsor
its development: it ensures the project that your product relies on
stays healthy and actively maintained. Individual users are also welcome
to make a recurring pledge or a one time donation if cfn-validator has
helped you in your work or personal projects.

Every single sign-up makes a significant impact towards making
cloudformation\_validator possible.

Want Custom Rules and Support For Your Application
--------------------------------------------------

Submit an issue on my github page if you would like additional custom
rules and I will try and get them added as soon as possible.

I you would like other functionality, just submit an issue and I will
see what I can do to get it added.

Installation
------------

cloudformation\_validator is on PyPI so all you need is:

``` {.sourceCode .console}
$ pip install cfn-validator
```

Testing
-------

Just run:

``` {.sourceCode .console}
$ python setup.py test
```

Or you can use tox to run the tests under all supported Python versions.
Make sure the required python versions are installed and run:

``` {.sourceCode .console}
$ pip install tox  # first time only
$ tox
```

Listing Rules
-------------

``` {.sourceCode .console}
$ cfn-validator dump_rules
##################################
########## WARNINGS ##############
##################################
{'id': 'F4', 'type': 'VIOLATION::WARNING', 'message': 'IAM policy should not allow * action'}
{'id': 'W1', 'type': 'VIOLATION::WARNING', 'message': 'Specifying credentials in the template itself is probably not the safest thing'}
...
```

Example
-------

Getting help

``` {.sourceCode .console}
$ cfn-validator validate --help
Usage: cfn-validator validate [OPTIONS]

  primary function for validating a template :param template_path: :param
  template_file: :param debug: :param rules_directory: :param profile_path:
  :param allow_suppression: :param print_suppression: :param
  parameter_values_path: :param isolate_custom_rule_exceptions: :param
  version: :return:

Options:
  -s, --suppress-errors           Whether to suppress misc errors to get hash only
  -t, --template-path TEXT        base directory to search for templates
  -f, --template-file TEXT        single_template_file
  --debug                         Turn on debugging
  -r, --rules-directory TEXT      Extra rule directory
  -o
```