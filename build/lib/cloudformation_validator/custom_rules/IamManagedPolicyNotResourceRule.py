from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - IamManagedPolicyNotResourceRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class IamManagedPolicyNotResourceRule(BaseRule):

    def __init__(self, cfn_model=None, debug=None):
        """
        Initialize IamManagedPolicyNotResourceRule
        :param cfn_model:
        """
        BaseRule.__init__(self, cfn_model, debug=debug)

    def rule_text(self):
        """
        Returns rule text
        :return:
        """
        return 'IAM managed policy should not allow Allow+NotResource'


    def rule_type(self):
        """
        Returns rule type
        :return:
        """
        self.type= 'VIOLATION::WARNING'
        return 'VIOLATION::WARNING'


    def rule_id(self):
        """
        Returns rule id
        :return:
        """
        if self.debug:
            print('rule_id'+lineno())
        self.id ='W23'
        return 'W23'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('IamManagedPolicyNotResourceRule - audit_impl'+lineno())

        violating_policies = []

        resources = self.cfn_model.resources_by_type('AWS::IAM::ManagedPolicy')

        if len(resources)>0:
            for resource in resources:
                if self.debug:
                    print('resource: '+str(resource))

                if hasattr(resource,'policy_document'):
                    if self.debug:
                        print('has policy document '+lineno())

                        print('policy document: '+str(resource.policy_document)+lineno())
                    if resource.policy_document:
                        if resource.policy_document.allows_not_resource():
                            if self.debug:
                                print('has allows not resource')

                            violating_policies.append(str(resource.logical_resource_id))

                else:
                    if self.debug:
                        print('does not have policy document'+lineno())

        else:
            if self.debug:
                print('no violating_policies' + lineno())

        return violating_policies