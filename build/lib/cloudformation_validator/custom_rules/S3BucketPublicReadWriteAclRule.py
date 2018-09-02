from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule

def lineno():
    """Returns the current line number in our program."""
    return str(' - S3BucketPublicReadWriteAclRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class S3BucketPublicReadWriteAclRule(BaseRule):
  
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
    return 'S3 Bucket should not have a public read-write acl'


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
    self.id ='F14'
    return 'F14'


  def audit_impl(self):
    """
    Audit
    :return: violations 
    """
    if self.debug:
      print('S3BucketPublicReadWriteAclRule - audit_impl'+lineno())
    logical_resource_ids = []

    resources = self.cfn_model.resources_by_type('AWS::S3::Bucket')

    if len(resources) > 0:
      for resource in resources:
        if self.debug:
          print('resource: ' + str(resource)+lineno())
          print('vars: '+str(vars(resource))+lineno())
        if hasattr(resource,'accessControl'):
          if resource.accessControl:
            if resource.accessControl == 'PublicReadWrite':
              logical_resource_ids.append(str(resource.logical_resource_id))

    else:
      if self.debug:
        print('no violating_policies' + lineno())

    return logical_resource_ids