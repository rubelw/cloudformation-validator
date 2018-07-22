cfn_validator
=========================


Features
--------
cfn_validator provides type checking and other base functionality out of the box and
is designed to be non-blocking and easily extensible, allowing for custom
validation. It has no dependencies and is thoroughly tested under Python 2.7, Python 3.3, Python 3.4,
Python 3.5, Python 3.6.

Funding
-------
cfn_validator is a open source, collaboratively funded project. If you run
a business and are using cfn_validator in a revenue-generating product, it would
make business sense to sponsor its development: it ensures the project that
your product relies on stays healthy and actively maintained. Individual users
are also welcome to make a recurring pledge or a one time donation if cfn-nagger
has helped you in your work or personal projects.

Every single sign-up makes a significant impact towards making cfn_validator possible.

Want Custom Rules and Support For Your Application
---------------------------------------------------
Submit an issue on my github page if you would like additional custom rules and I will try and
get them added as soon as possible.

I you would like other functionality, just submit an issue and I will see what I can do to get
it added.

Installation
------------

cfn_validator is on PyPI so all you need is:

.. code-block:: console

    $ pip install cfn-nagger

Testing
-------

Just run:

.. code-block:: console

    $ python setup.py test

Or you can use tox to run the tests under all supported Python versions. Make
sure the required python versions are installed and run:

.. code-block:: console

    $ pip install tox  # first time only
    $ tox

Listing Rules
---------------

.. code-block:: console

    $ cfn-nagger dump_rules
    ##################################
    ########## WARNINGS ##############
    ##################################
    {'id': 'F4', 'type': 'VIOLATION::WARNING', 'message': 'IAM policy should not allow * action'}
    {'id': 'W1', 'type': 'VIOLATION::WARNING', 'message': 'Specifying credentials in the template itself is probably not the safest thing'}
    ...

Example
---------

Getting help

.. code-block:: console

    $ cfn-nagger validate --help
    Usage: cfn-nagger validate [OPTIONS]

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


Validate a file

.. code-block:: console

    $cfn-nagger validate -f cloudfront_distribution_without_logging.json

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

Validate all files in a path

.. code-block:: console

    $cfn-nagger validate -f /projects
    ...


Programmatically call cfn-nagger to analyze a file

.. code-block:: console

    from cfn_validator.ValidateUtility import ValidateUtility

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

I you get some errors and warnings in your out put, you can pass-in the flag to suppress all errors

.. code-block:: console

    from cfn_validator.ValidateUtility import ValidateUtility

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

Writing your own rules

    * Utilize the format for existing rules in the /cfn_validator/custom_rules directory
    * Places the files in a new directory
    * The __init__, rule_text, rule_type and rule_id methods should be amount the same, just change of the rule, the text for a failure, and the type to either 'VIOLATION::FAILING_VIOLATION' or VIOLATION::WARNNING'
    * Set the id to 'W' for warnings, and 'F' for failure.  Pick a number not utilized elsewhere...
    * NOTE:  Currently working on functionality for controlling and listing rules
    * For the audit_impl function - portion with will test the resource objects, you will need to review the object model for the resource to see what objects are available, and then review the parser for the resource.  Also, look at other similar rules for the resource, and model after them.  The basic concept of the function is to identify resources which apply, iterate over the selected resources, and identify specific aspects to evaluate in the rule
    * pass in the --rules-directory /directory in the command line, and the extra rules directory will get added to the existing rules


.. code-block:: console

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

Unit Testing
------------------------
Run unit tests

.. code-block:: console

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


Source
---------

I am just getting started on this, so any suggestions would be welcome.
<https://github.com/rubelw/cfn-nagger>


Copyright
---------

cfn_validator is an open source project by Will Rubel <https://www.linkedin.com/in/will-rubel-03205b2a/>,
that was ported from a ruby project by Stelligent.
See the original LICENSE information <https://github.com/stelligent/cfn_nag/blob/master/LICENSE.md>.
