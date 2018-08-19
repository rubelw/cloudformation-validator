from __future__ import absolute_import, division, print_function
import sys
import inspect
from cfn_model.parser.PolicyDocumentParser import PolicyDocumentParser
from cfn_model.model.Policy import Policy


def lineno():
    """Returns the current line number in our program."""
    return str(' -  IamRoleParser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class IamRoleParser:
    """
    IAM Role Parser
    """
    
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse iam role
        :param resource: 
        :param debug: 
        :return: 
        """
        if debug:
            print('IAMRoleParser - parse'+lineno())
            print('resource: '+str(resource)+lineno())
            print('debug is: '+str(debug)+lineno())

        iam_role = resource

        document_parser =  PolicyDocumentParser(debug=debug)
        iam_role.assume_role_policy_document  =document_parser.parse(iam_role.assumeRolePolicyDocument)


        for policy in iam_role.policies:
            if debug:
                print('policy: '+str(policy)+lineno())

            if 'PolicyName' in policy:
                if debug:
                    print('has policy name: '+str(policy['PolicyName']))

                new_policy = Policy(debug=debug)
                new_policy.policy_name = policy['PolicyName']
                new_policy.policy_document = document_parser.parse(policy['PolicyDocument'])
                iam_role.policy_objects.append(new_policy)

        return iam_role