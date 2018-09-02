from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
  """Returns the current line number in our program."""
  return str(' -  CloudFormationAuthenticationRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class CloudFormationAuthenticationRule(BaseRule):

    def __init__(self, cfn_model=None, debug=None):
          """
          Initialize CloudFormationAuthenticationRule
          :param cfn_model:
          """
          BaseRule.__init__(self, cfn_model, debug=debug)

    def rule_text(self):
          """
          Returns rule text
          :return:
          """
          if self.debug:
            print('rule_text'+lineno())
          return 'Specifying credentials in the template itself is probably not the safest thing'


    def rule_type(self):
          """
          Returns the rule type
          :return:
          """
          self.type= 'VIOLATION::WARNING'
          return 'VIOLATION::WARNING'

    def rule_id(self):
          """
          Returns the rule_id
          :return:
          """
          if self.debug:
                print('rule_id'+lineno())
          self.id = 'W1'
          return 'W1'

    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('CloudFormationAuthnticationRule - audit_impl'+lineno())

        logical_resource_ids = []

        for resource in self.cfn_model.raw_model['Resources']:
            if self.debug:
                print('resource: '+str(resource)+lineno())
            if 'Metadata' in self.cfn_model.raw_model['Resources'][resource]:
                if self.debug:
                    print('found metadata')

                if 'AWS::CloudFormation::Authentication' in self.cfn_model.raw_model['Resources'][resource]['Metadata']:
                    if self.debug:
                        print('has authentication')

                    if self.potentially_sensitive_credentials(self.cfn_model.raw_model['Resources'][resource]['Metadata']['AWS::CloudFormation::Authentication']):
                        logical_resource_ids.append(str(resource))

        return logical_resource_ids

    def potentially_sensitive_credentials(self, auth):
        """
        Whether there are potentially sensitive credentials
        :param auth:
        :return:
        """
        if self.debug:
            print('potentially sensitive credentials'+lineno())

        # Example
        # "Metadata": {
        #   "AWS::CloudFormation::Authentication": {
        #     "testBasic" : {
        #       "type" : "basic",
        #       "username" : "biff",
        #       "password" : "badpassword",
        #       "uris" : [ "http://www.example.com/test" ]
        #     }
        #   }
        # }

        if type(auth) == type(dict()):
            for item in auth:

                if type(auth[item]) == type(dict()):

                    for item2 in auth[item]:
                        if self.debug:
                            print('item: '+str(item2))
                        if str(item2) in ['accessKeyId','password','secretKey']:
                            return True

        return False