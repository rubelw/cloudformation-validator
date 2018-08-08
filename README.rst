
Cloudformation-Validator
========================

Features
========

Cloudformation Validator validates cloudformation schemas and templates against
a variety of security and non-security rules, and provides type checking and other base
functionality out of the box and is designed to be non-blocking and
easily extensible, allowing for custom validation. It has no
dependencies and is thoroughly tested under Python 2.7, Python 3.3,
Python 3.4, Python 3.5, Python 3.6.

Funding
=======

Cloudformation Validator is a open source, collaboratively funded
project. If you run a business and are using cloudformation_validator in
a revenue-generating product, it would make business sense to sponsor
its development: it ensures the project that your product relies on
stays healthy and actively maintained. Individual users are also welcome
to make a recurring pledge or a one time donation if cfn-validator has
helped you in your work or personal projects.

Every single sign-up makes a significant impact towards making
Cloudformation Validator possible.

Want Custom Rules and Support For Your Application
==================================================

Submit an issue on my github page if you would like additional custom
rules and I will try and get them added as soon as possible.

I you would like other functionality, just submit an issue and I will
see what I can do to get it added.

Installation
============

cloudformation_validator is on PyPI so all you need is:

.. code:: console

   $ pip install cfn-validator

Testing
=======

Just run:

``{.sourceCode .console $ pip install virtualenv $ which python $ virtualenv ~/virtualenvs/my_project -p /home/example_username/opt/python-3.6.2/bin/python3 $ git clone https://github.com/rubelw/cloudformation-validator.git $ cd cloudformation-validator $ pip install -r requirements-dev.txt $ python setup.py install --force $ python setup.py test}``

Or you can use tox to run the tests under all supported Python versions.
Make sure the required python versions are installed and run:

``{.sourceCode .console $ pip install virtualenv $ which python $ virtualenv ~/virtualenvs/my_project -p /home/example_username/opt/python-3.6.2/bin/python3 $ git clone https://github.com/rubelw/cloudformation-validator.git $ cd cloudformation-validator $ pip install -r requirements-dev.txt $ python setup.py install --force $ pip install tox  # first time only $ tox}``

Listing Rules
=============

.. code:: console

   $ cfn-validator dump_rules
   ##################################
   ########## WARNINGS ##############
   ##################################
   {'id': 'F4', 'type': 'VIOLATION::WARNING', 'message': 'IAM policy should not allow * action'}
   {'id': 'W1', 'type': 'VIOLATION::WARNING', 'message': 'Specifying credentials in the template itself is probably not the safest thing'}
   ...


Excluding Certain Rules From Evaluation
=======================================

If you know that certain rules should be excluded, for example a load balancer with a security group open to 0.0.0.0/0, then exclude
the rule using the exclude rules option, and a commad delimited list.

.. code:: console

   cfn-validator validate --template-file=rds_instances_with_public_credentials.json --excluded-rules=F23,F24


Using an S3 Bucket For Custom Rules
===================================

If you want to store your organization's custom rules in an S3 bucket, then you must pass-in in s3-profile flag and
set the rules directory to the bucket name.

.. code:: console

   # Without a profile
   cfn-validator validate --template-file=template.json --s3-bucket-name=custom-rules
   # With a profile
   cfn-validator validate --template-file=template.json --s3-bucket-name=custom-rules --s3-profile=will


Disable PyPi Package Update Check
=================================

Cloudformation validator will automatically check for pypi updates.  To disable these automatic checks, pass-in
the --disable-pypi-check flag

.. code:: console

    cfn-validator validate --template-file=missing_one_required_tags.json --disable-pypi-check


Example
=======

Getting help

.. code:: console

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

Validate a file

.. code:: console

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

Validate all files in a path

.. code:: console

   $cfn-validator validate -f /projects
   ...

Programmatically call cfn-validator to analyze a file

.. code:: console

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

I you get some errors and warnings in your out put, you can pass-in the
flag to suppress all errors

.. code:: console

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

Writing your own rules

   -  Utilize the format for existing rules in the
      /cloudformation_validator/custom_rules directory
   -  Places the files in a new directory
   -  The \__init__, rule_text, rule_type and rule_id methods should be
      amount the same, just change of the rule, the text for a failure,
      and the type to either 'VIOLATION::FAILING_VIOLATION' or
      VIOLATION::WARNNING'
   -  Set the id to 'W' for warnings, and 'F' for failure. Pick a number
      not utilized elsewhere...
   -  NOTE: Currently working on functionality for controlling and
      listing rules
   -  For the audit_impl function - portion with will test the resource
      objects, you will need to review the object model for the resource
      to see what objects are available, and then review the parser for
      the resource. Also, look at other similar rules for the resource,
      and model after them. The basic concept of the function is to
      identify resources which apply, iterate over the selected
      resources, and identify specific aspects to evaluate in the rule
   -  pass in the --rules-directory /directory in the command line, and
      the extra rules directory will get added to the existing rules

.. code:: console

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

Example of writing a rule which requires custom tags for EC2 instances
======================================================================

-  Create a directory to store your custom rule
-  Create the custom rule

.. code:: console

   mkdir ~/custom_validator_rules

.. code:: console

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

-  Test the rule by creating a cloudformation template without the
   necessary tags and testing

.. code:: console

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

-  Run the test

``{.sourceCode .console cfn-validator validate --template-file=/tmp/template.json --rules-directory=/home/user/custom_validator_rules}``

-  You should receive the following violations

.. code:: console

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

-  Now, add tags property to the cloudformation template and run again

``{.sourceCode .console { "Parameters": { "subnetId": { "Type": "String", "Default": "subnet-4fd01116" } },} "Resources": {   "EC2I4LBA1": {     "Type": "AWS::EC2::Instance",     "Properties": {       "ImageId": "ami-6df1e514",       "InstanceType": "t2.micro",       "SubnetId": {         "Ref": "subnetId"       },       "Tags" : [         {"Key" : "Name", "Value":"value"},         {"Key":"ResourceOwner","Value":"resourceowner"},         {"Key":"DeployedBy","Value":"deployedby"},         {"Key":"Project","Value":"project"}       ]     },     "Metadata": {       "AWS::CloudFormation::Authentication": {         "testBasic" : {           "type" : "basic",           "username" : "biff",           "password" : "badpassword",           "uris" : [ "http://www.example.com/test" ]         }       }     }   } }``


-  You should receive the following violations

``{.sourceCode .console { 'failure_count': '0', 'filename': '/tmp/template.json', 'file_results': [ { 'id': 'W1', 'type': 'VIOLATION::WARNING', 'message': 'Specifying credentials in the template itself is probably not the safest thing', 'logical_resource_ids': [ 'EC2I4LBA1' ] } ] }}``

Unit Testing
============

Run unit tests

.. code:: console

   (python3) => tox
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

   ...
   Name                                                                                      Stmts   Miss  Cover
   -------------------------------------------------------------------------------------------------------------
   cfn_model/__init__.py                                                                         0      0   100%
   cfn_model/model/CfnModel.py                                                                 128     72    44%
   cfn_model/model/EC2Instance.py                                                                9      0   100%
   cfn_model/model/EC2NetworkInterface.py                                                       11     11     0%
   cfn_model/model/EC2SecurityGroup.py                                                          11      0   100%
   cfn_model/model/EC2SecurityGroupEgress.py                                                     9      1    89%
   cfn_model/model/EC2SecurityGroupIngress.py                                                    9      1    89%
   cfn_model/model/ElasticLoadBalancingLoadBalancer.py                                          17      0   100%
   cfn_model/model/ElasticLoadBalancingV2LoadBalancer.py                                        11      7    36%
   cfn_model/model/IAMGroup.py                                                                   9      5    44%
   cfn_model/model/IAMManagedPolicy.py                                                          12      7    42%
   cfn_model/model/IAMPolicy.py                                                                  9      5    44%
   cfn_model/model/IAMRole.py                                                                   10      0   100%
   cfn_model/model/IAMUser.py                                                                   10      0   100%
   cfn_model/model/LambdaPrincipal.py                                                           13      0   100%
   cfn_model/model/ModelElement.py                                                              35     18    49%
   cfn_model/model/Parameter.py                                                                 26     13    50%
   cfn_model/model/Policy.py                                                                    12      2    83%
   cfn_model/model/PolicyDocument.py                                                           114     43    62%
   cfn_model/model/Principal.py                                                                 56     21    63%
   cfn_model/model/References.py                                                                90     57    37%
   cfn_model/model/S3BucketPolicy.py                                                             7      0   100%
   cfn_model/model/SNSTopicPolicy.py                                                             9      0   100%
   cfn_model/model/SQSQueuePolicy.py                                                             8      0   100%
   cfn_model/model/Statement.py                                                                105     66    37%
   cfn_model/model/__init__.py                                                                   0      0   100%
   cfn_model/parser/CfnParser.py                                                               340    162    52%
   cfn_model/parser/Ec2InstanceParser.py                                                        29     15    48%
   cfn_model/parser/Ec2NetworkInterfaceParser.py                                                10      3    70%
   cfn_model/parser/Error.py                                                                    17     10    41%
   cfn_model/parser/IamGroupParser.py                                                           27     17    37%
   cfn_model/parser/IamRoleParser.py                                                            28      6    79%
   cfn_model/parser/IamUserParser.py                                                            48     30    38%
   cfn_model/parser/LoadBalancerParser.py                                                       26     11    58%
   cfn_model/parser/LoadBalancerV2Parser.py                                                     11      4    64%
   cfn_model/parser/ParserError.py                                                              24      7    71%
   cfn_model/parser/ParserRegistry.py                                                           20      2    90%
   cfn_model/parser/PolicyDocumentParser.py                                                    126     66    48%
   cfn_model/parser/SecurityGroupParser.py                                                     254    122    52%
   cfn_model/parser/TransformRegistry.py                                                        23      9    61%
   cfn_model/parser/WithPolicyDocumentParser.py                                                 18      4    78%
   cfn_model/parser/__init__.py                                                                  0      0   100%
   cfn_model/transforms/Serverless.py                                                           47     33    30%
   cfn_model/transforms/__init__.py                                                              0      0   100%
   cfn_model/validator/CloudformationValidator.py                                               40     18    55%
   cfn_model/validator/ReferenceValidator.py                                                   156     79    49%
   cfn_model/validator/ResourceTypeValidator.py                                                 34     13    62%
   cfn_model/validator/SchemaGenerator.py                                                       81     20    75%
   cfn_model/validator/__init__.py                                                               0      0   100%
   cloudformation_validator/CustomRuleLoader.py                                                272    130    52%
   cloudformation_validator/IpAddr.py                                                          714    564    21%
   cloudformation_validator/Profile.py                                                          22      6    73%
   cloudformation_validator/ProfileLoader.py                                                    58     23    60%
   cloudformation_validator/RuleDefinition.py                                                   27     14    48%
   cloudformation_validator/RuleDumper.py                                                       39     27    31%
   cloudformation_validator/RuleRegistry.py                                                     70     33    53%
   cloudformation_validator/TemplateDiscovery.py                                                40     30    25%
   cloudformation_validator/ValidateUtility.py                                                 384    172    55%
   cloudformation_validator/Violation.py                                                        35      9    74%
   cloudformation_validator/__init__.py                                                          9      0   100%
   cloudformation_validator/additional_custom_rules/EbsCustomTagsRule.py                        56     11    80%
   cloudformation_validator/additional_custom_rules/Ec2CustomTagsRule.py                        57     11    81%
   cloudformation_validator/additional_custom_rules/RdsCustomTagsRule.py                        57     11    81%
   cloudformation_validator/additional_custom_rules/S3CustomTagsRule.py                         57     11    81%
   cloudformation_validator/additional_custom_rules/__init__.py                                  0      0   100%
   cloudformation_validator/command.py                                                         109     60    45%
   cloudformation_validator/custom_rules/BaseRule.py                                            31      9    71%
   cloudformation_validator/custom_rules/CloudFormationAuthenticationRule.py                    50      9    82%
   cloudformation_validator/custom_rules/CloudFrontDistributionAccessLoggingRule.py             42      9    79%
   cloudformation_validator/custom_rules/EbsVolumeHasSseRule.py                                 47     11    77%
   cloudformation_validator/custom_rules/ElasticLoadBalancerAccessLoggingRule.py                38      7    82%
   cloudformation_validator/custom_rules/IamManagedPolicyNotActionRule.py                       46     20    57%
   cloudformation_validator/custom_rules/IamManagedPolicyNotResourceRule.py                     43     18    58%
   cloudformation_validator/custom_rules/IamManagedPolicyWildcardActionRule.py                  52     26    50%
   cloudformation_validator/custom_rules/IamManagedPolicyWildcardResourceRule.py                50     24    52%
   cloudformation_validator/custom_rules/IamPolicyNotActionRule.py                              43     16    63%
   cloudformation_validator/custom_rules/IamPolicyNotResourceRule.py                            42     16    62%
   cloudformation_validator/custom_rules/IamPolicyWildcardActionRule.py                         42     16    62%
   cloudformation_validator/custom_rules/IamPolicyWildcardResourceRule.py                       42     16    62%
   cloudformation_validator/custom_rules/IamRoleNotActionOnPermissionsPolicyRule.py             47     13    72%
   cloudformation_validator/custom_rules/IamRoleNotActionOnTrustPolicyRule.py                   47     16    66%
   cloudformation_validator/custom_rules/IamRoleNotPrincipalOnTrustPolicyRule.py                44     15    66%
   cloudformation_validator/custom_rules/IamRoleNotResourceOnPermissionsPolicyRule.py           47     13    72%
   cloudformation_validator/custom_rules/IamRoleWildcardActionOnPermissionsPolicyRule.py        46     11    76%
   cloudformation_validator/custom_rules/IamRoleWildcardActionOnTrustPolicyRule.py              46     13    72%
   cloudformation_validator/custom_rules/IamRoleWildcardResourceOnPermissionsPolicyRule.py      59     17    71%
   cloudformation_validator/custom_rules/LambdaPermissionInvokeFunctionActionRule.py            42     13    69%
   cloudformation_validator/custom_rules/LambdaPermissionWildcardPrincipalRule.py               42      9    79%
   cloudformation_validator/custom_rules/ManagedPolicyOnUserRule.py                             40     14    65%
   cloudformation_validator/custom_rules/PolicyOnUserRule.py                                    37     11    70%
   cloudformation_validator/custom_rules/RDSInstanceMasterUserPasswordRule.py                   62     18    71%
   cloudformation_validator/custom_rules/RDSInstanceMasterUsernameRule.py                       64     19    70%
   cloudformation_validator/custom_rules/RDSInstancePubliclyAccessibleRule.py                   40      8    80%
   cloudformation_validator/custom_rules/S3BucketPolicyNotActionRule.py                         44     11    75%
   cloudformation_validator/custom_rules/S3BucketPolicyNotPrincipalRule.py                      42     10    76%
   cloudformation_validator/custom_rules/S3BucketPolicyWildcardActionRule.py                    43      9    79%
   cloudformation_validator/custom_rules/S3BucketPolicyWildcardPrincipalRule.py                 44      9    80%
   cloudformation_validator/custom_rules/S3BucketPublicReadAclRule.py                           39      7    82%
   cloudformation_validator/custom_rules/S3BucketPublicReadWriteAclRule.py                      39      7    82%
   cloudformation_validator/custom_rules/SecurityGroupEgressOpenToWorldRule.py                  50     16    68%
   cloudformation_validator/custom_rules/SecurityGroupEgressPortRangeRule.py                    60     26    57%
   cloudformation_validator/custom_rules/SecurityGroupIngressCidrNon32Rule.py                  132     76    42%
   cloudformation_validator/custom_rules/SecurityGroupIngressOpenToWorldRule.py                 57     19    67%
   cloudformation_validator/custom_rules/SecurityGroupIngressPortRangeRule.py                   65     22    66%
   cloudformation_validator/custom_rules/SecurityGroupMissingEgressRule.py                      36      7    81%
   cloudformation_validator/custom_rules/SnsTopicPolicyNotActionRule.py                         41      9    78%
   cloudformation_validator/custom_rules/SnsTopicPolicyNotPrincipalRule.py                      39      8    79%
   cloudformation_validator/custom_rules/SnsTopicPolicyWildcardPrincipalRule.py                 48     13    73%
   cloudformation_validator/custom_rules/SqsQueuePolicyNotActionRule.py                         43      9    79%
   cloudformation_validator/custom_rules/SqsQueuePolicyNotPrincipalRule.py                      43     11    74%
   cloudformation_validator/custom_rules/SqsQueuePolicyWildcardActionRule.py                    40      8    80%
   cloudformation_validator/custom_rules/SqsQueuePolicyWildcardPrincipalRule.py                 40      8    80%
   cloudformation_validator/custom_rules/UserHasInlinePolicyRule.py                             35      8    77%
   cloudformation_validator/custom_rules/UserMissingGroupRule.py                                38      8    79%
   cloudformation_validator/custom_rules/WafWebAclDefaultActionRule.py                          40     14    65%
   cloudformation_validator/custom_rules/__init__.py                                             0      0   100%
   cloudformation_validator/result_views/JsonResults.py                                        107     43    60%
   cloudformation_validator/result_views/RulesView.py                                           49     38    22%
   cloudformation_validator/result_views/SimpleStdoutResults.py                                 17      8    53%
   cloudformation_validator/result_views/__init__.py                                             0      0   100%
   -------------------------------------------------------------------------------------------------------------
   TOTAL                                                                                      6557   2863    56%

Source
======

I am just getting started on this, so any suggestions would be welcome.
<https://github.com/rubelw/cloudformation-validator>


Copyright
=========

cloudformation_validator is an open source project by Will Rubel
<https://www.linkedin.com/in/will-rubel-03205b2a/>, that was ported from
a ruby project by Stelligent. See the original LICENSE information
<https://github.com/stelligent/cfn_nag/blob/master/LICENSE.md>.
