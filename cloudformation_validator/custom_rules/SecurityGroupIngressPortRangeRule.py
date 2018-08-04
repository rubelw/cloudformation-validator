from __future__ import absolute_import, division, print_function
import copy
import sys
import inspect
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupIngressPortRangeRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class SecurityGroupIngressPortRangeRule(BaseRule):

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
        return 'Security Groups found ingress with port range instead of just a single port'


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
        self.id ='W27'
        return 'W27'



    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('SecurityGroupIngressPortRangeRule - audit_impl'+lineno())

        violating_ingresses = []

        for groups in self.cfn_model.security_groups():

            if self.debug:
                print('group: '+str(groups)+lineno())

            if type(groups)==type(dict()):
                if str(groups['FromPort']) != str(groups['ToPort']):
                    violating_ingresses.append(groups.logical_resource_id)

            else:
                if self.debug:
                    print('ingress is not a dict: '+lineno())

                for ingress in groups.ingresses:
                    if self.debug:
                        print('## ingresses: '+str(ingress)+lineno())

                    if type(ingress)==type(dict()):

                        if str(ingress['FromPort']) != str(ingress['ToPort']):
                            violating_ingresses.append(groups.logical_resource_id)

                    elif type(ingress) == type(list()):

                        for item in ingress:

                            if type(item) == type(dict()):

                                if str(item['FromPort']) != str(item['ToPort']):
                                    violating_ingresses.append(str(groups.logical_resource_id))

                            elif item.fromPort != item.toPort:
                                violating_ingresses.append(str(item.logical_resource_id))

                    elif ingress.fromPort != ingress.toPort:
                        violating_ingresses.append(str(ingress.logical_resource_id))

        violating_standalone_ingresses = self.cfn_model.standalone_ingress()
        if self.debug:
            print('violating standalone ingresses: '+str(violating_standalone_ingresses)+lineno())

        for groups in violating_standalone_ingresses:
            if self.debug:
                print('group: '+str(groups)+lineno())
                print('vars: '+str(vars(groups))+lineno())

            if hasattr(groups,'cfn_model'):
                if 'Properties' in groups.cfn_model:
                    if 'ToPort' in groups.cfn_model['Properties'] and 'FromPort' in groups.cfn_model['Properties']:

                        if str(groups.cfn_model['Properties']['ToPort']) != str(groups.cfn_model['Properties']['FromPort']):
                            violating_ingresses.append(str(groups.logical_resource_id))

        if self.debug:
            print('violations: '+str(list(set(violating_ingresses))))

        return violating_ingresses