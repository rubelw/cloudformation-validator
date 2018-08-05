from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - UserHasInlinePolicyRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))

class UserHasInlinePolicyRule(BaseRule):


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
      return 'IAM user should not have any inline policies.  Should be centralized Policy object on group'


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
      self.id ='F10'
      return 'F10'


  def audit_impl(self):
      """
      Audit
      :return: violations
      """
      if self.debug:
          print('UserHasInlinePolicyRule - audit_impl'+lineno())

      violating_users = []

      for user in self.cfn_model.iam_users():
          if self.debug:
              print('user: '+str(user))
              print('vars: '+str(vars(user))+lineno())
          if hasattr(user,'policy_objects'):
              if user.policy_objects:
                  if len(user.policy_objects)>0:
                      violating_users.append(str(user.logical_resource_id))

      return violating_users