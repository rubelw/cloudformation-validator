from __future__ import absolute_import, division, print_function
import inspect
import sys
from cfn_model.parser.PolicyDocumentParser import PolicyDocumentParser
from cfn_model.model.Policy import Policy


def lineno():
    """Returns the current line number in our program."""
    return str(' -  IamUserParser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class IamUserParser:
    """
    IAM User Parser
    """

    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse iam user
        :param resource: 
        :param debug: 
        :return: 
        """

        if debug:
            print('parse'+lineno())

        iam_user = resource

        for policy in iam_user.policies:
            if debug:
                print('policy: '+str(policy)+lineno())

            new_policy = Policy(debug=debug)
            new_policy.policy_name = policy['PolicyName']
            policy_document_parser =PolicyDocumentParser()
            new_policy.policy_document=policy_document_parser.parse(policy['PolicyDocument'])

            iam_user.policy_objects.append(new_policy)

        for group_name in iam_user.groups:
            if debug:
                print('group_name: '+str(group_name)+lineno())
            iam_user.group_names.append(group_name)

        user_to_group_additions = cfn_model.resources_by_type('AWS::IAM::UserToGroupAddition')

        if debug:
            print('user_to_group_additions: '+str(user_to_group_additions)+lineno())

        for user_to_group_addition in user_to_group_additions:
            if IamUserParser.user_to_group_addition_has_username(user_to_group_addition.users,iam_user,debug=debug):
                iam_user.group_names = user_to_group_addition.groupName
                #    # we need to figure out the story on resolving Refs i think for this to be real

        return iam_user



    def user_to_group_addition_has_username(addition_user_names, user_to_find, debug=False):
        """
        ???
        :param user_to_find: 
        :param debug: 
        :return: 
        """
        if debug:
            print('user_to_group_addition_has_username'+lineno())
            print('user names: '+str(addition_user_names)+lineno())
            print('user to find: '+str(user_to_find)+lineno())

        for addition_user_name in addition_user_names:

            if debug:
                print('vars: '+str(vars(user_to_find))+lineno())

            if hasattr(user_to_find,'userName'):
                if addition_user_name == user_to_find.userName:
                    return True

            if type(addition_user_name) == type(dict()):
                if 'Ref' in addition_user_name:
                    if addition_user_name['Ref'] == user_to_find.logical_resource_id:
                        return True

        return False