from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' -  IamManagedPolicyWildcardResourceRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class IamManagedPolicyWildcardResourceRule(BaseRule):

  def __init__(self, cfn_model=None, debug=None):
    """
    Initialize IamManagedPolicyWildcardResourceRule
    :param cfn_model: 
    """
    BaseRule.__init__(self, cfn_model, debug=debug)

  def rule_text(self):
    """
    Return rule text
    :return: 
    """
    if self.debug:
        print('rule_text'+lineno())
    return 'IAM managed policy should not allow * resource'


  def rule_type(self):
    """
    Return rule type
    :return: 
    """
    self.type= 'VIOLATION::WARNING'
    return 'VIOLATION::WARNING'


  def rule_id(self):
    """
    Return rule id
    :return: 
    """
    if self.debug:
        print('rule_id'+lineno())
    self.id ='W13'
    return 'W13'


  def audit_impl(self):
    """
    Audit
    :return:  violations 
    """
    if self.debug:
        print('IamMangedPolicyWildcardResourceRule - audit_impl'+lineno())

    violating_policies = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::ManagedPolicy')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
              print('resources: '+str(resource)+lineno())
              print('vars: '+str(vars(resource))+lineno())
          if hasattr(resource,'policy_document'):
            if self.debug:
                print('has policy document '+lineno())
                print('vars: '+str(vars(resource.policy_document)))

            if resource.policy_document:
                if self.debug:
                    print(resource.policy_document.statements)

                for statements in resource.policy_document.statements:
                    if self.debug:
                        print('statements: '+str(statements))
                        print('vars: '+str(vars(statements)))

                if resource.policy_document.wildcard_allowed_resources():
                    if self.debug:
                        print('has wildcard allow resources')

                    violating_policies.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_policies' + lineno())


    return violating_policies