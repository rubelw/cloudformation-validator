from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupEgressPortRangeRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class SecurityGroupEgressPortRangeRule(BaseRule):


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
    return 'Security Groups found egress with port range instead of just a single port'


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
    self.id ='W29'
    return 'W29'


  ##
  # This will behave slightly different than the legacy jq based rule which was targeted against inline ingress only
  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
        print('SecurityGroupEgressPortRangeRule - audit_impl'+lineno())
    violating_egresses = []

    for groups in self.cfn_model.security_groups():

        if self.debug:
            print('group: '+str(groups)+lineno())

        if type(groups)==type(dict()):
            if str(groups['FromPort']) != str(groups['ToPort']):
                violating_egresses.append(groups.logical_resource_id)

        else:

            for egress in groups.egresses:
              if self.debug:
                print('## egresses: '+str(egress))

              if type(egress)==type(dict()):

                if str(egress['FromPort']) != str(egress['ToPort']):
                    violating_egresses.append(str(groups.logical_resource_id))

              elif type(egress) == type(list()):

                  for item in egress:

                      if type(item) == type(dict()):

                          if str(item['FromPort']) != str(item['ToPort']):
                              violating_egresses.append(groups.logical_resource_id)

                      elif hasattr(item,'fromPort') and hasattr(item,'toPort') and item.fromPort != item.toPort:
                          violating_egresses.append(str(item.logical_resource_id))

              elif hasattr(egress,'fromPort') and hasattr(egress,'toPort') and egress.fromPort != egress.toPort:
                violating_egresses.append(str(egress.logical_resource_id))

    violating_standalone_egresses = self.cfn_model.standalone_egress()
    if self.debug:
        print('violating standalone egresses: '+str(violating_standalone_egresses)+lineno())

    # For standalone egress resource types
    for groups in violating_standalone_egresses:
        if self.debug:
            print('group: '+str(groups)+lineno())
            print('vars: '+str(vars(groups))+lineno())

        if hasattr(groups,'cfn_model'):
            if 'Properties' in groups.cfn_model:
                if 'ToPort' in groups.cfn_model['Properties'] and 'FromPort' in groups.cfn_model['Properties']:

                    if str(groups.cfn_model['Properties']['ToPort']) != str(groups.cfn_model['Properties']['FromPort']):
                        violating_egresses.append(str(groups.logical_resource_id))

    return violating_egresses