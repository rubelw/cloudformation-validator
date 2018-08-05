from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleNotActionOnTrustPolicyRule- caller: '+str(inspect.stack()[1][3])+'  - line number: '+str(inspect.currentframe().f_back.f_lineno))



class IamRoleNotActionOnTrustPolicyRule(BaseRule):
  

  def __init__(self, cfn_model=None, debug=None):
    """
    Initialize
    :param cfn_model: 
    """
    BaseRule.__init__(self, cfn_model,debug=debug)

  def rule_text(self):
    """
    Get rule text
    :return: 
    """
    if self.debug:
      print('rule_text'+lineno())
    return 'IAM role should not allow Allow+NotAction on trust permissions'
  

  def rule_type(self):
    """
    Get rule type
    :return: 
    """
    self.type= 'VIOLATION::WARNING'
    return 'VIOLATION::WARNING'
  

  def rule_id(self):
    """
    Get rule id
    :return: 
    """
    if self.debug:
      print('rule_id'+lineno())
    self.id ='W14'
    return 'W14'
  

  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('IamRoleNotActionOnTrustPolicyRule - audit_impl'+lineno())

    dir(self.cfn_model)
    if self.debug:
      print('vars: '+str(vars(self))+lineno())
      print('dir: '+str(dir(self))+lineno())
      print('cfn_model: '+str(self.cfn_model)+lineno())

    violating_roles = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::Role')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())

          if hasattr(resource, 'policy_document'):
            if self.debug:
              print('has policy document ' + lineno())

              print(resource.policy_document.policy_document.statements)
            if resource.policy_document.policy_document.allows_not_action():
                if self.debug:
                  print('has allows not action')

                violating_roles.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_roles' + lineno())

    return violating_roles