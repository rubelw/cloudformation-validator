from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - RDSInstanceMasterUserPasswordRule- caller: '+str(inspect.stack()[1][3])+'  - line number: '+str(inspect.currentframe().f_back.f_lineno))


class RDSInstanceMasterUserPasswordRule(BaseRule):
  
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
    return 'RDS instance master user password must be Ref to NoEcho Parameter. Default credentials are not recommended'


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
    self.id ='F23'
    return 'F23'


  # one word of warning... if somebody applies parameter values via JSON.... this will compare that....
  # probably shouldn't be doing that though - if it's NoEcho there's a good reason
  # bother checking synthesized_value? that would be the indicator.....
  def audit_impl(self):
    """
    Audit
    :return: violations
    """
    if self.debug:
      print('RDSInstanceMasterUserPasswordRule - audit_impl'+lineno())
    
    violating_rdsinstances = []

    resources = self.cfn_model.resources_by_type('AWS::RDS::DBInstance')

    if len(resources)>0:
      for resource in resources:
          if self.debug:
            print('resource: '+str(resource)+lineno())
            print('vars:'+str(vars(resource))+lineno())

          if hasattr(resource,'masterUserPassword'):

            if resource.masterUserPassword:

              if not self.references_no_echo_parameter_without_default(self.cfn_model,resource.masterUserPassword):
                 violating_rdsinstances.append(str(resource.logical_resource_id))

              if self.debug:
                print('violating_rdsinstances: ' + str(violating_rdsinstances) + lineno())

    else:
      if self.debug:
        print('no violating_rdsinstances' + lineno())

    return violating_rdsinstances

  def to_boolean(self,string):
    """
    Why and how used
    :param string: 
    :return: 
    """
    if self.debug:
      print('to_boolean'+lineno())
    # FIXME
    sys.exit(1)
    #string.to_s.casecmp('true').zero?


  def references_no_echo_parameter_without_default(self,cfn_model, master_user_password):
    """
    ???
    :param cfn_model: 
    :param master_user_password: 
    :return: 
    """
    if self.debug:
      print('references_no_echo_parameter_without_default'+lineno())
      print('cfn_model: '+str(vars(cfn_model))+lineno())
      print('master_username: '+str(master_user_password)+lineno())

    if type(master_user_password) == type(dict()):

      if 'Ref' in master_user_password:
        if hasattr(cfn_model,'parameters'):
          if str(master_user_password['Ref']) in cfn_model.parameters:
            parameter = cfn_model.parameters[master_user_password['Ref']]

            if hasattr(parameter,'NoEcho'):
              if self.debug:
                print('has noecho property: '+lineno())
              return True

    if self.debug:
      print('Does not have noecho property '+lineno())
        
    return False