from __future__ import absolute_import, division, print_function
import inspect
import sys
import time
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from cloudformation_validator.IpAddr import IpAddr


def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupIngressOpenToWorldRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class SecurityGroupIngressOpenToWorldRule(BaseRule):
  

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
        return 'Security Groups found with cidr open to world on ingress.  This should never be true on instance.  Permissible on ELB'


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
        self.id ='W2'
        return 'W2'



    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('SecurityGroupIngressOpenToWorldRule - audit_impl'+lineno())
        violating_ingresses = []

        for groups in self.cfn_model.security_groups():
            if self.debug:
                print('group: '+str(groups)+lineno())
                print('vars: '+str(vars(groups))+lineno())

            for ingress in groups.ingresses:
                if self.debug:
                    print('ingress: '+str(ingress)+lineno())
                    print('type: '+str(type(ingress)))

                if type(ingress)== type(dict()):
                    if IpAddr.ip4_open(ingress,debug=self.debug) or IpAddr.ip6_open(ingress,debug=self.debug):
                        if self.debug:
                            print('ip4/6 address is open'+lineno())
                        violating_ingresses.append(str(groups.logical_resource_id))
                else:
                    if IpAddr.ip4_open(ingress,debug=self.debug) or IpAddr.ip6_open(ingress,debug=self.debug):
                        if self.debug:
                            print('ip4/6 address is open'+lineno())
                        violating_ingresses.append(str(ingress.logical_resource_id))

        routes= self.cfn_model.standalone_ingress()

        if self.debug:
            print('routes: '+str(routes)+lineno())
        for standalone_ingress in routes:
            if self.debug:
                print('standalone_ingress: '+str(standalone_ingress)+lineno())
                print('vars: '+str(vars(standalone_ingress))+lineno())

            if IpAddr.ip4_open(standalone_ingress,debug=self.debug) or IpAddr.ip6_open(standalone_ingress,debug=self.debug):
                if self.debug:
                    print('ip4/6 address is open' + lineno())
                violating_ingresses.append(str(standalone_ingress.logical_resource_id))

        return violating_ingresses