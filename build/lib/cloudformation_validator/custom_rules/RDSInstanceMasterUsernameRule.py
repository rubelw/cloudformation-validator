from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - RDSInstanceMasterUsernameRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


# cfn_nag rules related to RDS Instance master username
class RDSInstanceMasterUsernameRule(BaseRule):

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
      return 'RDS instance master username must be Ref to NoEcho Parameter. Default credentials are not recommended'


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
      self.id ='F24'
      return 'F24'



  def audit_impl(self):
      """
      # Warning: if somebody applies parameter values via JSON, this will compare
      # that....
      # probably shouldn't be doing that though -
      # if it's NoEcho there's a good reason
      # bother checking synthesized_value? that would be the indicator.....
      :return: violations
      """
      if self.debug:
          print('RDSInstanceMasterUsernameRule - audit_impl'+lineno())
    
      violating_rdsinstances = []

      resources = self.cfn_model.resources_by_type('AWS::RDS::DBInstance')

      if len(resources)>0:
          for resource in resources:
              if self.debug:
                  print('resource: '+str(resource)+lineno())
                  print('resource: '+str(vars(resource))+lineno())

              if hasattr(resource,'masterUsername'):
                  if self.debug:
                      print('has masterUsername resource')
                  if resource.masterUsername:

                      if not self.references_no_echo_parameter_without_default(self.cfn_model,resource.masterUsername):
                          violating_rdsinstances.append(str(resource.logical_resource_id))

                      if self.debug:
                          print('violating_rdsinstances: ' + str(violating_rdsinstances) + lineno())

      else:
          if self.debug:
              print('no violating_rdsinstances' + lineno())


      return violating_rdsinstances

  def to_boolean(self, string):
    """
    Not sure why
    :param string:
    :return:
    """
    if self.debug:
      print('to_boolean'+lineno())

    # FIXME
    sys.exit(1)
    #if string.to_s.casecmp('true').zero?
    #  true
    #else
    #  false
    #end


  def references_no_echo_parameter_without_default(self, cfn_model, master_username):
    """
    No echo parameter without defaults
    :param cfn_model:
    :param master_username:
    :return:
    """
    if self.debug:
      print('references_no_ech_parameter_without_default'+lineno())
      print('cfn_model: '+str(vars(cfn_model))+lineno())
      print('master_username: '+str(master_username)+lineno())

    if type(master_username) == type(dict()):

      if 'Ref' in master_username:
        if hasattr(cfn_model,'parameters'):
          if str(master_username['Ref']) in cfn_model.parameters:
            parameter = cfn_model.parameters[master_username['Ref']]

            if hasattr(parameter,'NoEcho'):
              if self.debug:
                print('has noecho property: '+lineno())
              return True


    if self.debug:
      print('Does not have noecho property '+lineno())
    return False