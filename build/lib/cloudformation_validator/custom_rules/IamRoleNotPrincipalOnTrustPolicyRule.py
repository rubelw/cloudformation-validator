from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleNotPrincipalOnTrustPolicyRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class IamRoleNotPrincipalOnTrustPolicyRule(BaseRule):
  
  def __init__(self, cfn_model=None, debug=None):
    """
    Initialize
    :param cfn_model: 
    """
    BaseRule.__init__(self, cfn_model, debug=debug)

  def rule_text(self):
    """
    Get rule text
    :return: 
    """
    if self.debug:
      print('rule_text'+lineno())
    return 'IAM role should not allow Allow+NotPrincipal in its trust policy'
  

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
    self.id ='F6'
    return 'F6'
  

  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('IamRoleNotPrincipalOnTrustPolicyRule - audit_impl'+lineno())

      print('vars: '+str(vars(self)))
      print('dir: '+str(dir(self)))

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
            if resource.policy_document.policy_document.allows_not_principal():
                if self.debug:
                  print('has allows not principal')

                violating_roles.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_roles' + lineno())

    return violating_roles