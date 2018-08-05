from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.Violation import Violation
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleNotResourceOnPermissionsPolicyRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class IamRoleNotResourceOnPermissionsPolicyRule(BaseRule):

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
    return 'IAM role should not allow Allow+NotResource'


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
    self.id ='W21'
    return 'W21'


  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('IamRoleNotResourceOnPermissionPolicyRule - audit_impl'+lineno())

      print('vars: '+str(vars(self)))
      print('dir: '+str(dir(self)))

    violating_roles = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::Role')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())

          if hasattr(resource, 'policy_objects'):
            if self.debug:
              print('has policy obects ' + lineno())

            for policy in resource.policy_objects:

              if policy.policy_document.allows_not_resource():
                if self.debug:
                  print('has allows not resources')

                violating_roles.append(str(resource.logical_resource_id))
    else:
      if self.debug:
        print('no violating_roles' + lineno())

    if self.debug:
      print('returning violating_roles to'+lineno())
        
    return violating_roles