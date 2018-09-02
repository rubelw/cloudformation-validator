from __future__ import absolute_import, division, print_function
import inspect
import sys
from cfn_model.model.IAMPolicy import IAMPolicy
from cfn_model.model.PolicyDocument import PolicyDocument
from cfn_model.parser.PolicyDocumentParser import PolicyDocumentParser


def lineno():
    """Returns the current line number in our program."""
    return str(' -  WithPolicyDocumentParser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class WithPolicyDocumentParser:
    """
    With policy document parser
    """
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse with policy document parser
        :param resource:
        :param debug:
        :return:
        """
        if debug:
            print('parse'+lineno())
            print('resource: '+str(resource))
            print('vars: '+str(vars(resource)))
        parser = PolicyDocumentParser(debug)
        resource.policy_document = parser.parse(resource.policyDocument)

        return resource
