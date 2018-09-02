from __future__ import absolute_import, division, print_function
import sys
import copy
import inspect
from cfn_model.model.Policy import Policy
from cfn_model.parser.PolicyDocumentParser import PolicyDocumentParser

def lineno():
    """Returns the current line number in our program."""
    return str(' -  IamGroupParser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class IamGroupParser:
    """
    IAM group parser
    """
    
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse iam group
        :param resource: 
        :param debug: 
        :return: 
        """
        if debug:
            print('IAMGroupParser - parse'+lineno())
            print('resource: '+str(resource)+lineno())

        iam_group = copy.copy(resource)

        if debug:
            print('attributes: '+str(vars(iam_group))+lineno())

        for policy in iam_group.policies:
            if debug:
                print('policy: '+str(policy)+lineno())

            if 'Policies' in policy:
                if len(policy['Policies'])>0:

                    new_policy = Policy(debug=debug)
                    new_policy.name = policy['PolicyName']
                    new_policy.policy_document = PolicyDocumentParser.parse(policy['PolicyDocument'])

                    iam_group.policy_objects.append(new_policy)

        return iam_group