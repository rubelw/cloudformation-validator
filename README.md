---
title: 'cloudformation\_validator'
---

Features
========

cloudformation\_validator provides type checking and other base
functionality out of the box and is designed to be non-blocking and
easily extensible, allowing for custom validation. It has no
dependencies and is thoroughly tested under Python 2.7, Python 3.3,
Python 3.4, Python 3.5, Python 3.6.

Funding
=======

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
==================================================

Submit an issue on my github page if you would like additional custom
rules and I will try and get them added as soon as possible.

I you would like other functionality, just submit an issue and I will
see what I can do to get it added.

Installation
============

cloudformation\_validator is on PyPI so all you need is:

``` {.sourceCode .console}
$ pip install cfn-validator
```

Testing
=======

Just run:

``` {.sourceCode .console
$ pip install virtualenv
$ which python
$ virtualenv ~/virtualenvs/my_project -p /home/example_username/opt/python-3.6.2/bin/python3
$ git clone https://github.com/rubelw/cloudformation-validator.git
$ cd cloudformation-validator
$ pip install -r requirements-dev.txt
$ python setup.py install --force
$ python setup.py test}
```

Or you can use tox to run the tests under all supported Python versions.
Make sure the required python versions are installed and run:

``` {.sourceCode .console
$ pip install virtualenv
$ which python
$ virtualenv ~/virtualenvs/my_project -p /home/example_username/opt/python-3.6.2/bin/python3
$ git clone https://github.com/rubelw/cloudformation-validator.git
$ cd cloudformation-validator
$ pip install -r requirements-dev.txt
$ python setup.py install --force
$ pip install tox  # first time only
$ tox}
```

Listing Rules
=============

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
=======

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
  -o, --profile-path TEXT         Path to a profile file
  --allow-suppression / --no-allow-suppression
                                  Allow using Metadata to suppress violations
  -p, --print-suppression         Emit suppressions to stderr
  -m, --parameter-values-path TEXT
                                  Path to a JSON file to pull Parameter values
                                  from
  -i, --isolate-custom-rule-exceptions
                                  Isolate custom rule exceptions - just emit
                                  the exception without stack trace and keep
                                  chugging
  -v, --version                   Print version and exit
  --help                          Show this message and exit.
```

Validate a file

``` {.sourceCode .console}
$cfn-validator validate -f cloudfront_distribution_without_logging.json

Evaluating: cloudfront_distribution_without_logging.json
[
    {
        'failure_count': '0',
        'filename': 'cloudfront_distribution_without_logging.json',
        'file_results': [
            {
                'id': 'W10',
                'type': 'VIOLATION::WARNING',
                'message': 'CloudFront Distribution should enable access logging',
                'logical_resource_ids': [
                    'rDistribution2'
                ]
            }
        ]
    }
]
```

Validate all files in a path

``` {.sourceCode .console}
$cfn-validator validate -f /projects
...
```

Programmatically call cfn-validator to analyze a file

``` {.sourceCode .console}
from cloudformation_validator.ValidateUtility import ValidateUtility

config_dict = {}
config_dict['template_file'] = '/tmp/template.json'
validator = ValidateUtility(config_dict)
real_result =  validator.validate()
print(real_result)

[
    {
        'failure_count': '0',
        'filename': '/tmp/template.json',
        'file_results': [
            {
                'id': 'W1',
                'type': 'VIOLATION::WARNING',
                'message': 'Specifying credentials in the template itself is probably not the safest thing',
                'logical_resource_ids': [
                    'EC2I4LBA1'
                ]
            }
        ]
    }
]
```

I you get some errors and warnings in your out put, you can pass-in the
flag to suppress all errors

``` {.sourceCode .console}
from cloudformation_validator.ValidateUtility import ValidateUtility

config_dict = {}
config_dict['suppress_errors'] = True
config_dict['template_file'] = '/tmp/template.json'
validator = ValidateUtility(config_dict)
real_result =  validator.validate()
print(real_result)

[
    {
        'failure_count': '0',
        'filename': '/tmp/template.json',
        'file_results': [
            {
                'id': 'W1',
                'type': 'VIOLATION::WARNING',
                'message': 'Specifying credentials in the template itself is probably not the safest thing',
                'logical_resource_ids': [
                    'EC2I4LBA1'
                ]
            }
        ]
    }
]
```

Writing your own rules

> -   Utilize the format for existing rules in the
>     /cloudformation\_validator/custom\_rules directory
> -   Places the files in a new directory
> -   The \_\_init\_\_, rule\_text, rule\_type and rule\_id methods
>     should be amount the same, just change of the rule, the text for a
>     failure, and the type to either \'VIOLATION::FAILING\_VIOLATION\'
>     or VIOLATION::WARNNING\'
> -   Set the id to \'W\' for warnings, and \'F\' for failure. Pick a
>     number not utilized elsewhere\...
> -   NOTE: Currently working on functionality for controlling and
>     listing rules
> -   For the audit\_impl function - portion with will test the resource
>     objects, you will need to review the object model for the resource
>     to see what objects are available, and then review the parser for
>     the resource. Also, look at other similar rules for the resource,
>     and model after them. The basic concept of the function is to
>     identify resources which apply, iterate over the selected
>     resources, and identify specific aspects to evaluate in the rule
> -   pass in the \--rules-directory /directory in the command line, and
>     the extra rules directory will get added to the existing rules

``` {.sourceCode .console}
def audit_impl(self):

  violating_rules = []

  # This defines which type of resource we are going to test
  resources = self.cfn_model.resources_by_type('AWS::SQS::QueuePolicy')

  if len(resources)>0:
    for resource in resources:
        if hasattr(resource, 'policy_document'):
          if resource.policy_document:
            if resource.policy_document.wildcard_allowed_actions():
              violating_rules.append(resource.logical_resource_id)

  return violating_rules
```

Example of writing a rule which requires custom tags for EC2 instances
======================================================================

-   Create a directory to store your custom rule
-   Create the custom rule

``` {.sourceCode .console}
mkdir ~/custom_validator_rules
```

``` {.sourceCode .console}
from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from collections import Iterable
from six import StringIO, string_types
from builtins import (str)

class Ec2CustomTagsRule(BaseRule):

  def __init__(self, cfn_model=None, debug=None):
    '''
    Initialize Ec2HasTagsRule
    :param cfn_model:
    '''
    BaseRule.__init__(self, cfn_model, debug=debug)

  def rule_text(self):
    '''
    Returns rule text
    :return:
    '''
    if self.debug:
      print('rule_text')
    return 'EC2 instance does not have the required tags'

  def rule_type(self):
    '''
    Returns rule type
    :return:
    '''
    self.type= 'VIOLATION::FAILING_VIOLATION'
    return 'VIOLATION::FAILING_VIOLATION'

  def rule_id(self):
    '''
    Returns rule id
    :return:
    '''
    if self.debug:
      print('rule_id')
    self.id ='F86'
    return 'F86'

  def tags_to_dict(self, aws_tags):
        """ Convert a list of AWS tags into a python dict """
        return {str(tag['Key']): str(tag['Value']) for tag in self.ensure_list(aws_tags)}

  def ensure_list(self, value):
        """
        Coerces a variable into a list; strings will be converted to a singleton list,
        and `None` or an empty string will be converted to an empty list.
        Args:
            value: a list, or string to be converted into a list.

        Returns:
            :py:class:`list`
        """
        ret_value = value
        if not value:
            ret_value = []
        elif not isinstance(value, Iterable) or isinstance(value, string_types):
            ret_value = [value]
        return ret_value


  def audit_impl(self):
    '''
    Audit
    :return: violations
    '''
    if self.debug:
      print('Ec2HasTagsRule - audit_impl')

    violating_volumes = []

    resources = self.cfn_model.resources_by_type('AWS::EC2::Instance')

    if len(resources) > 0:

      for resource in resources:
        if self.debug:
          print('resource: ' + str(resource))
          print('vars: '+str(vars(resource)))

        if hasattr(resource, 'tags'):
          tags_dict = self.tags_to_dict(resource.cfn_model['Properties']['Tags'])
          required_tags = ('Name', 'ResourceOwner','DeployedBy','Project')
          if not set(required_tags).issubset(tags_dict):
            violating_volumes.append(str(resource.logical_resource_id))
        else:
          if self.debug:
            print('does not tags property')
          violating_volumes.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_volumes')

    return violating_volumes
```

-   Test the rule by creating a cloudformation template without the
    necessary tags and testing

``` {.sourceCode .console}
{
  "Parameters": {
    "subnetId": {
      "Type": "String",
      "Default": "subnet-4fd01116"
    }
  },

  "Resources": {
    "EC2I4LBA1": {
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "ImageId": "ami-6df1e514",
        "InstanceType": "t2.micro",
        "SubnetId": {
          "Ref": "subnetId"
        }
      },
      "Metadata": {
        "AWS::CloudFormation::Authentication": {
          "testBasic" : {
            "type" : "basic",
            "username" : "biff",
            "password" : "badpassword",
            "uris" : [ "http://www.example.com/test" ]
          }
        }
      }
    }
  }
}
```

-   Run the test

``` {.sourceCode .console
cfn-validator validate --template-file=/tmp/template.json --rules-directory=/home/user/custom_validator_rules}
```

-   You should receive the following violations

``` {.sourceCode .console}
{
    'failure_count': '1',
    'filename': '/tmp/template.json',
    'file_results': [
        {
            'id': 'F86',
            'type': 'VIOLATION::FAILING_VIOLATION',
            'message': 'EC2 instance does not have the required tags',
            'logical_resource_ids': [
                'EC2I4LBA1'
            ]
        },
        {
            'id': 'W1',
            'type': 'VIOLATION::WARNING',
            'message': 'Specifying credentials in the template itself is probably not the safest thing',
            'logical_resource_ids': [
                'EC2I4LBA1'
            ]
        }
    ]
}
```

-   No add tags property to the cloudformation template and run again

``` {.sourceCode .console
{
"Parameters": {
"subnetId": {
"Type": "String",
"Default": "subnet-4fd01116"
}
},}
"Resources": {
  "EC2I4LBA1": {
    "Type": "AWS::EC2::Instance",
    "Properties": {
      "ImageId": "ami-6df1e514",
      "InstanceType": "t2.micro",
      "SubnetId": {
        "Ref": "subnetId"
      },
      "Tags" : [
        {"Key" : "Name", "Value":"value"},
        {"Key":"ResourceOwner","Value":"resourceowner"},
        {"Key":"DeployedBy","Value":"deployedby"},
        {"Key":"Project","Value":"project"}
      ]
    },
    "Metadata": {
      "AWS::CloudFormation::Authentication": {
        "testBasic" : {
          "type" : "basic",
          "username" : "biff",
          "password" : "badpassword",
          "uris" : [ "http://www.example.com/test" ]
        }
      }
    }
  }
}
```

> }

-   You should receive the following violations

``` {.sourceCode .console
{
'failure_count': '0',
'filename': '/tmp/template.json',
'file_results': [
{
'id': 'W1',
'type': 'VIOLATION::WARNING',
'message': 'Specifying credentials in the template itself is probably not the safest thing',
'logical_resource_ids': [
'EC2I4LBA1'
]
}
]
}}
```

Unit Testing
============

Run unit tests

``` {.sourceCode .console}
(python3) => pytest
================================================ test session starts =================================================
collected 22 items

test/test_cloudfront_distribution.py .                                                                         [  4%]
test/test_ec2_instance.py .                                                                                    [  9%]
test/test_ec2_volume.py ..                                                                                     [ 18%]
test/test_elasticloadbalancing_loadbalancer.py .                                                               [ 22%]
test/test_iam_user.py .                                                                                        [ 27%]
test/test_lambda_permission.py .                                                                               [ 31%]
test/test_rds_instance.py ...                                                                                  [ 45%]
test/test_s3_bucket.py .                                                                                       [ 50%]
test/test_s3_bucket_policy.py .                                                                                [ 54%]
test/test_security_group.py ........                                                                           [ 90%]
test/test_sns_policy.py .                                                                                      [ 95%]
test/test_sqs_policy.py .                                                                                      [100%]
```

Source
======

I am just getting started on this, so any suggestions would be welcome.
\<<https://github.com/rubelw/cloudformation-validator>\>

Copyright
=========

cloudformation\_validator is an open source project by Will Rubel
\<<https://www.linkedin.com/in/will-rubel-03205b2a/>\>, that was ported
from a ruby project by Stelligent. See the original LICENSE information
\<<https://github.com/stelligent/cfn_nag/blob/master/LICENSE.md>\>.
