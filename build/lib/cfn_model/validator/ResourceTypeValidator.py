from __future__ import absolute_import, division, print_function
import inspect
from cfn_model.parser import ParserError

def lineno():
    """Returns the current line number in our program."""
    return str(' -  ResourceTypeValidator- line number: '+str(inspect.currentframe().f_back.f_lineno))


class ResourceTypeValidator:
    """
    Resource Type Validator
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug:
        """
        self.debug=debug
        if self.debug:
            print('ResourceTypeValidator - init'+lineno())

    def validate(self, cloudformation_yml):
        """
        validate cloud formation
        :param cloudformation_yml:
        :return:
        """

        if self.debug:
            print("\n\n########################################")
            print('ResourceTypeValidator - validate'+lineno())
            print('Iterating through each of the resources and validating them')
            print("############################################\n\n")

        if 'Resources' not in cloudformation_yml:

            raise ParserError.ParserError('Illegal cfn - no Resources')
        else:
            if self.debug:
                print('cloudformation has resources'+lineno())

        for resources in cloudformation_yml['Resources']:

            if self.debug:
                print('resource: '+str(resources))
            if 'Type' not in cloudformation_yml['Resources'][resources]:
                raise ParserError.ParserError('Illegal cfn - missing Type: id: '+str(resources))
            else:
                if self.debug:
                    print('resource: '+str(resources)+' has type'+lineno())

        if 'Parameters' in cloudformation_yml:
            for parameter in cloudformation_yml['Parameters']:
                if 'Type' not in cloudformation_yml['Parameters'][parameter]:
                    raise ParserError.ParserError('Illegal cfn - missing Parameter Type: id: ' + str(parameter))

                else:
                    if self.debug:
                        print('parameter: '+str(parameter)+' has type'+lineno())


        return cloudformation_yml