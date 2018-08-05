from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' - RDSInstancePubliclyAccessibleRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class RDSInstancePubliclyAccessibleRule(BaseRule):
  
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
    return 'RDS instance should not be publicly accessible'


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
    self.id ='F22'
    return 'F22'


  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('RDSInstancePubliclyAccessibleRule - audit_impl'+lineno())
    
    violating_rdsinstances = []
    
    resources = self.cfn_model.resources_by_type('AWS::RDS::DBInstance')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())
            print('resource: '+str(vars(resource))+lineno())

          if hasattr(resource,'publiclyAccessible'):
            if self.debug:
              print('has publiclyAssible attribute')

            if str(resource.publiclyAccessible) == 'True' or str(resource.publiclyAccessible)=='true':
                  violating_rdsinstances.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_rdsinstances' + lineno())

    return violating_rdsinstances