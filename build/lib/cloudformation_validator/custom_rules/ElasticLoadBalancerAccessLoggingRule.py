from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule



def lineno():
    """Returns the current line number in our program."""
    return str(' - ElasticLoadBalancerAccessLoggingRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class ElasticLoadBalancerAccessLoggingRule(BaseRule):

    def __init__(self, cfn_model=None, debug=None):
        """
        Initialize ElasticLoadBalancerAccessLoggingRule
        :param cfn_model:
        """
        BaseRule.__init__(self, cfn_model, debug=debug)

    def rule_text(self):
        """
        Returns rule text
        :return:
        """
        if self.debug:
            print('rule_text'+lineno())
        return 'Elastic Load Balancer should have access logging enabled'


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
        self.id ='W26'
        return 'W26'

    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('ElasticLoadBalancerAccessLoggingRule - audit_impl'+lineno())

        violating_elbs = []
        resources = self.cfn_model.resources_by_type('AWS::ElasticLoadBalancing::LoadBalancer')

        if len(resources) > 0:
            for resource in resources:
                if self.debug:
                    print('resource: ' + str(resource)+lineno())
                    print('vars: '+str(vars(resource))+lineno())

                if hasattr(resource,'accessLoggingPolicy'):
                    if resource.accessLoggingPolicy == None or ('Enabled' in resource.accessLoggingPolicy and resource.accessLoggingPolicy['Enabled'] != True):
                        violating_elbs.append(str(resource.logical_resource_id))

        else:
            if self.debug:
                print('no violating_elbs'+lineno())


        return violating_elbs