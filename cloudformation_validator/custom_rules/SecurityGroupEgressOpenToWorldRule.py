from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from cloudformation_validator.IpAddr import IpAddr

def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupEgressOpenToWorldRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class SecurityGroupEgressOpenToWorldRule(BaseRule):
  

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
    return 'Security Groups found with cidr open to world on egress'


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
    self.id ='W5'
    return 'W5'


  ##
  # This will behave slightly different than the legacy jq based rule which was targeted against inline ingress only
  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
        print('SecurityGroupEgressOpenToWorldRule - audit_impl'+lineno())
    violating_egresses = []

    for groups in self.cfn_model.security_groups():
        if self.debug:
            print('group: '+str(groups)+lineno())
            print('vars: '+str(vars(groups))+lineno())

        for egress in groups.egresses:
            if self.debug:
                print('egress: '+str(egress)+lineno())

            if IpAddr.ip4_open(egress, debug=self.debug) or IpAddr.ip6_open(egress, debug=self.debug):
              if self.debug:
                print('ip4/6 address is open'+lineno())
              violating_egresses.append(str(groups.logical_resource_id))

    routes= self.cfn_model.standalone_egress()

    if self.debug:
        print('routes: '+str(routes)+lineno())
    for standalone_egress in routes:
      if self.debug:
        print('standalone_egress: '+str(standalone_egress)+lineno())
        print('vars: '+str(vars(standalone_egress))+lineno())

      if IpAddr.ip4_open(standalone_egress,debug=self.debug) or IpAddr.ip6_open(standalone_egress,debug=self.debug):
        if self.debug:
            print('ip4/6 address is open' + lineno())
        violating_egresses.append(standalone_egress.logical_resource_id)

    return violating_egresses
