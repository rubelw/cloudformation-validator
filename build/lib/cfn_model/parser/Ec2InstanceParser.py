from __future__ import absolute_import, division, print_function
import copy
import inspect
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' -  Ec2InstanceParser- line number: '+str(inspect.currentframe().f_back.f_lineno))


class Ec2InstanceParser:
    """
    Ec2 instance parser
    """
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse ec2 instances resources
        :param resource: 
        :param debug: 
        :return: 
        """

        if debug:
            print('Ec2InstancePaRSER - parse'+lineno())

        ec2_instance = copy.copy(resource)

        if hasattr(ec2_instance,'securityGroupIds'):
            if type(ec2_instance.securityGroupIds) == type(list()):

                for sg in ec2_instance.securityGroupIds:

                    if debug:
                        print('security group: '+str(sg)+lineno())
                        print('type: '+str(type(sg))+lineno())

                    if type(sg)== type(list()):
                        if debug:
                            print('security group is a list'+lineno())
                        sys.exit(1)
                    else:
                        if debug:
                            print('security group is not a list - it is a '+str(type(sg))+lineno())

                        if 'Ref' in sg:
                            ec2_instance.security_groups = cfn_model.find_security_group_by_group_id(sg['Ref'])

            else:

                print('FIXME')
                # could be a Ref to a List<AWS::EC2::SecurityGroup::Id> which we can't
                # do much with at the level of static analysis before knowing the parameter passed in
                # worth checking defaults?
                ec2_instance.security_groups = []

        return ec2_instance