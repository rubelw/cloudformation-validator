from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - UserMissingGroupRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class UserMissingGroupRule(BaseRule):

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
        return 'User is not assigned to a group'


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
        self.id ='F2000'
        return 'F2000'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('UserMissingGroupRule - audit_impl'+lineno())
        logical_resource_ids = []

        for user in self.cfn_model.iam_users():
            if self.debug:
                print('user: '+str(user))
                print('vars: '+str(vars(user)))

            if hasattr(user, 'group_names'):
                if self.debug:
                    print('hass group_names attribute'+lineno())

                if len(user.group_names)<1:

                    if self.debug:
                        print('no group names')

                    logical_resource_ids.append(str(user.logical_resource_id))


        return logical_resource_ids

