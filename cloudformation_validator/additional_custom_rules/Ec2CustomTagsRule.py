from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from collections import Iterable
from six import StringIO, string_types
from builtins import (str)


def lineno():
    """Returns the current line number in our program."""
    return str(' -  Ec2HasTagsRule - caller: ' + str(inspect.stack()[1][3]) + ' - line number: ' + str(
        inspect.currentframe().f_back.f_lineno))

class Ec2CustomTagsRule(BaseRule):
    """
    Ec2 custom tags rule
    """
    
    def __init__(self, cfn_model=None, debug=None):
        """
        Initialize Ec2HasTagsRule
        :param cfn_model:
        """
        BaseRule.__init__(self, cfn_model, debug=debug)

    def rule_text(self):
        """
        Returns rule text
        :return:
        """
        if self.debug:
            print('rule_text' + lineno())
        return 'EC2 instance does not have the required tags of Name, ResourceOwner, DeployedBy, Project'

    def rule_type(self):
        """
        Returns rule type
        :return:
        """
        self.type = 'VIOLATION::FAILING_VIOLATION'
        return 'VIOLATION::FAILING_VIOLATION'

    def rule_id(self):
        """
        Returns rule id
        :return:
        """
        if self.debug:
            print('rule_id' + lineno())
        self.id = 'F86'
        return 'F86'

    def tags_to_dict(self, aws_tags):
        """ Convert a list of AWS tags into a python dict """
        return {str(tag['Key']): str(tag['Value']) for tag in self.ensure_list(aws_tags)}

    def ensure_list(self, value):
        """
        Coerces a variable into a list; strings will be converted to a singleton list,
        and `None` or an empty string will be converted to an empty list.
        Args:
            value: a list, or string to be converted into a list.

        Returns:
            :py:class:`list`
        """
        ret_value = value
        if not value:
            ret_value = []
        elif not isinstance(value, Iterable) or isinstance(value, string_types):
            ret_value = [value]
        return ret_value

    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('Ec2HasTagsRule - audit_impl' + lineno())

        violating_volumes = []

        resources = self.cfn_model.resources_by_type('AWS::EC2::Instance')

        if len(resources) > 0:

            for resource in resources:
                if self.debug:
                    print('resource: ' + str(resource) + lineno())
                    print('vars: ' + str(vars(resource)))

                if hasattr(resource, 'tags'):
                    if self.debug:
                        print('has tags attribute' + lineno())

                    tags_dict = self.tags_to_dict(resource.cfn_model['Properties']['Tags'])

                    required_tags = ('Name', 'ResourceOwner', 'DeployedBy', 'Project')
                    if not set(required_tags).issubset(tags_dict):
                        violating_volumes.append(str(resource.logical_resource_id))
                else:
                    if self.debug:
                        print('does not tags property')
                    violating_volumes.append(str(resource.logical_resource_id))

        else:
            if self.debug:
                print('no violating_volumes' + lineno())

        return violating_volumes
