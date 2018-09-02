from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupMissingEgressRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class SecurityGroupMissingEgressRule(BaseRule):

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
        return 'Missing egress rule means all traffic is allowed outbound.  Make this explicit if it is desired configuration'


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
        self.id ='F1000'
        return 'F1000'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('SecurityGroupMissingEgressRule - audit_impl'+lineno())
        logical_resource_ids = []

        for groups in self.cfn_model.security_groups():
            if self.debug:
                print('group: '+str(groups)+lineno())
                print('vars:'+str(vars(groups))+lineno())

            if hasattr(groups,'egresses'):
                  if len(groups.egresses)<1:

                    logical_resource_ids.append(str(groups.logical_resource_id))

        if self.debug:
            print('violations: '+str(list(set(logical_resource_ids)))+lineno())

        return logical_resource_ids