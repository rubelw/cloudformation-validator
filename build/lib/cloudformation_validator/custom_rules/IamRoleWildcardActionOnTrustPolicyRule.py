from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleWildcardActionOnTrustPolicyRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))

class IamRoleWildcardActionOnTrustPolicyRule(BaseRule):

  def __init__(self, cfn_model=None, debug=None):
    """
    Initialize
    :param cfn_model: 
    """
    BaseRule.__init__(self, cfn_model,debug=debug)
      
  def rule_text(self):
    """
    Return rule text
    :return: 
    """
    if self.debug:
      print('rule_text'+lineno())
    return 'IAM role should not allow * action on its trust policy'


  def rule_type(self):
    """
    Get rule type
    :return: 
    """
    self.type= 'VIOLATION::FAILING_VIOLATION'
    return 'VIOLATION::FAILING_VIOLATION'


  def rule_id(self):
    """
    Get rule id
    :return: 
    """
    if self.debug:
      print('rule_id'+lineno())
    self.id ='F2'
    return 'F2'


  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('IamRoleWildcardActionOnTrustPolicyRule - audit_impl'+lineno())

    violating_roles = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::Role')

    if len(resources)>0:
      for resource in resources:
        if self.debug:
          print('resource: '+str(resource)+lineno())
          print('vars: '+str(vars(resource))+lineno())

        if hasattr(resource, 'assume_role_policy_document'):
          if self.debug:
            print('has assume role policy document ' + lineno())

          if resource.assume_role_policy_document:
            if self.debug:
              print('policy document: '+str(resource.assume_role_policy_document)+lineno())
              print('vars: '+str(resource.assume_role_policy_document)+lineno())


            if resource.assume_role_policy_document.wildcard_allowed_actions():
              if self.debug:
                print('has wildcard allowed actions')

              violating_roles.append(str(resource.logical_resource_id))
    else:
      if self.debug:
        print('no violating_roles'+lineno())

    return violating_roles