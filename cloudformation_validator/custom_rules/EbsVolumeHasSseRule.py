from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule



def lineno():
    """Returns the current line number in our program."""
    return str(' -  EbsVolumeHasSseRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



class EbsVolumeHasSseRule(BaseRule):

    def __init__(self, cfn_model=None, debug=None):
        """
        Initialize EbsVolumeHasSseRule
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
        return 'EBS volume should have server-side encryption enabled'

    def rule_type(self):
        """
        Returns rule type
        :return:
        """
        self.type= 'VIOLATION::FAILING_VIOLATION'
        return 'VIOLATION::FAILING_VIOLATION'

    def rule_id(self):
        """
        Returns rule id
        :return:
        """
        if self.debug:
            print('rule_id'+lineno())
        self.id ='F1'
        return 'F1'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('EbsVolumeHasSseRule - audit_impl'+lineno())

        violating_volumes = []

        resources = self.cfn_model.resources_by_type('AWS::EC2::Volume')

        if len(resources) > 0:

            for resource in resources:
                if self.debug:
                    print('resource: ' + str(resource)+lineno())
                    print('vars: '+str(vars(resource)))

                if hasattr(resource, 'encrypted'):
                    if self.debug:
                        print('has encrypted attribute'+lineno())
                    if resource.encrypted == 'true' or resource.encrypted == 'True':
                        if self.debug:
                            print('it is true')
                    else:
                        if self.debug:
                            print('not true')
                        violating_volumes.append(str(resource.logical_resource_id))
                else:
                    if self.debug:
                        print('does not have encrypted property')
                    violating_volumes.append(str(resource.logical_resource_id))

        else:
            if self.debug:
                print('no violating_volumes'+lineno())

        return violating_volumes