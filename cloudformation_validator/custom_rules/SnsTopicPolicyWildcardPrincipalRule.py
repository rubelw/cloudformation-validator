from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - SnsTopicPolicyWildcardPrincipalRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class SnsTopicPolicyWildcardPrincipalRule(BaseRule):


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
        return 'SNS topic policy should not allow * principal'


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
        self.id ='F18'
        return 'F18'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('SnsTopicPolicyWildcardPrincipalRul - audit_impl'+lineno())
        logical_resource_ids = []

        resources = self.cfn_model.resources_by_type('AWS::SNS::TopicPolicy')

        if len(resources)>0:
            for resource in resources:
                if self.debug:
                    print("\n\n##########################################")
                    print(str(dir(resource))+lineno())
                    print('resource: '+str(resource)+lineno())
                    print("##############################################\n")

                if hasattr(resource,'policy_document'):
                    if self.debug:
                        print('has policy document '+lineno())
                    if resource.policy_document:
                        if self.debug:
                            print('vars: '+str(vars(resource.policy_document))+lineno())

                        if resource.policy_document.wildcard_allowed_principals(debug=self.debug):
                            if self.debug:
                                print('has allows wildcard principals'+lineno())
                                print('resource id:'+str(resource.logical_resource_id)+lineno())

                            logical_resource_ids.append(str(resource.logical_resource_id))

        else:
            if self.debug:
                print('no violating_policies' + lineno())

        return logical_resource_ids