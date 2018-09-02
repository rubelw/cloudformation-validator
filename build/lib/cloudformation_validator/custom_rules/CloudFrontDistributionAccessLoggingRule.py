from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule


def lineno():
    """Returns the current line number in our program."""
    return str(' -  CloudFrontDistributionAccessLoggingRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))



# Rule class to ensure a CF distribution has logging
class CloudFrontDistributionAccessLoggingRule(BaseRule):

    def __init__(self, cfn_model=None, debug=None):
        """
        Initialize CloudFrontDistributionAccessLoggingRule
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
        return 'CloudFront Distribution should enable access logging'


    def rule_type(self):
        """
        Returns rule type
        :return:
        """
        self.type= 'VIOLATION::WARNING'
        return 'VIOLATION::WARNING'

    def rule_id(self):
        """
        Returns the rule id
        :return:
        """
        if self.debug:
            print('rule_id'+lineno())
        self.id = 'W10'
        return 'W10'

    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('CloudFrontDistributionAccessLoggingRule - audit_impl'+lineno())

        violating_distributions = []
        resources = self.cfn_model.resources_by_type('AWS::CloudFront::Distribution')

        if len(resources)>0:
            for resource in resources:
                if self.debug:
                    print('resource: '+str(resource)+lineno())

                if hasattr(resource, 'distributionConfig'):
                    if self.debug:
                        print('has distributionConfig ' + lineno())

                        print(resource.distributionConfig)
                    if 'Logging' not in resource.distributionConfig:
                        if self.debug:
                            print('does not have logging')

                        violating_distributions.append(str(resource.logical_resource_id))

        else:
            if self.debug:
                print('no violating_distributions'+lineno())

        return violating_distributions