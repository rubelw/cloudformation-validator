from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.Violation import Violation
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleNotActionOnPermissionsPolicyRule- caller: '+str(inspect.stack()[1][3])+'  - line number: '+str(inspect.currentframe().f_back.f_lineno))


class IamRoleNotActionOnPermissionsPolicyRule(BaseRule):

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
    return 'IAM role should not allow Allow+NotAction'


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
    self.id ='W15'
    return 'W15'


  def audit_impl(self):
    """
    Audit
    :return: violations
    """
    if self.debug:
      print('IamRoleNotActionOnPermissionsPolicyRule - audit_impl'+lineno())

    violating_roles = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::Role')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())

          if hasattr(resource,'policy_objects'):
            if self.debug:
              print('has policy obects '+lineno())

            for policy in resource.policy_objects:
              if self.debug:
                print('policy: '+str(policy))
                print('vars: '+str(vars(policy))+lineno())
                print('vars: ' + str(vars(policy.policy_document)) + lineno())

              if policy.policy_document.allows_not_action(debug=self.debug):
                if self.debug:
                  print('has allows not action')

                violating_roles.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_roles' + lineno())

    return violating_roles