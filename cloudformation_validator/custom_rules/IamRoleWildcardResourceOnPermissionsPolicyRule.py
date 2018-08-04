from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - IamRoleWildcardResourceOnPermissionsPolicyRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class IamRoleWildcardResourceOnPermissionsPolicyRule(BaseRule):


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
    return 'IAM role should not allow * resource on its permissions policy'

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
    self.id ='W11'
    return 'W11'


  def audit_impl(self):
    """
    Audit
    :return: violations
    """
    if self.debug:
      print('IamRoleWildcardResourceOnPermissionsPolicyRule - audit_impl'+lineno())

    dir(self.cfn_model)
    if self.debug:
      print('vars: '+str(vars(self))+lineno())
      print('dir: '+str(dir(self))+lineno())
      print('cfn_model: '+str(self.cfn_model)+lineno())

    violating_roles = []

    resources = self.cfn_model.resources_by_type('AWS::IAM::Role')

    if self.debug:
      print('IamRoleWildcardResourceOnPermissionsPolicyRule - audit_impl - violating_roles: '+str(violating_roles)+lineno())

    if len(resources)>0:
      for resource in resources:
        if self.debug:
          print('resources: ' + str(resource) + lineno())
          print('vars: ' + str(vars(resource)) + lineno())

        if hasattr(resource, 'policy_objects'):
          if self.debug:
            print('has policy obects ' + lineno())
            print('vars:'+str(resource.policy_objects)+lineno())

          if resource.policy_objects:

            for policy in resource.policy_objects:
              if self.debug:
                print('policy:'+str(policy))
                print('vars: '+str(vars(policy))+lineno())
              if hasattr(policy,'policy_document'):
                if self.debug:
                  print('has policy document attribute')
                if policy.policy_document:
                  if policy.policy_document.wildcard_allowed_resources():
                    if self.debug:
                      print('has wildcard allowed resources')

                    violating_roles.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_roles'+lineno())

    return violating_roles