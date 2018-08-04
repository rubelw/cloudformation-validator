from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from  cfn_model.model.LambdaPrincipal import LambdaPrincipal

def lineno():
    """Returns the current line number in our program."""
    return str(' - LambdaPermissionWildcardPrincipalRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class LambdaPermissionWildcardPrincipalRule(BaseRule):
  

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
    return 'Lambda permission principal should not be wildcard'


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
    self.id ='F13'
    return 'F13'


  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('LambdaPermissionWildcardPrincipalRule - audit_impl'+lineno())
    
    violating_lambdas = []
    
    resources = self.cfn_model.resources_by_type('AWS::Lambda::Permission')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())
            print('vars: '+str(vars(resource))+lineno())

          if hasattr(resource, 'principal'):
            if self.debug:
              print('has lambda principal ' + lineno())

              print(resource.principal)
            if LambdaPrincipal.wildcard(resource.principal):
              violating_lambdas.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_lambda' + lineno())

    return violating_lambdas
