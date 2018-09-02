from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)
from cloudformation_validator.custom_rules.BaseRule import BaseRule
from cloudformation_validator.IpAddr import IpAddr



def lineno():
    """Returns the current line number in our program."""
    return str(' - SecurityGroupIngressCidrNon32Rule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class SecurityGroupIngressCidrNon32Rule(BaseRule):

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
        return 'Security Groups found with ingress cidr that is not /32'


    def rule_type(self):
        """
        Get rule type
        :return:
        """
        self.type= 'VIOLATION::WARNING'
        return 'VIOLATION::WARNING'


    def rule_id(self):
        """
        Get rule id
        :return:
        """
        if self.debug:
          print('rule_id'+lineno())
        self.id ='W9'
        return 'W9'


    def audit_impl(self):
        """
        Audit
        :return: violations
        """
        if self.debug:
            print('SecurityGroupIngressCidrNon32Rule - audit_impl'+lineno())
        logical_resource_ids = []

        # Iterate over each of the security groups in the cloudformation template
        for groups in self.cfn_model.security_groups():

            if self.debug:
                print('group: '+str(groups)+lineno())
                print('vars: '+str(vars(groups))+lineno())

            # If the security group has ingresses
            if hasattr(groups,'ingresses'):
                if len(groups.ingresses)>0:

                    has_invalid_cidr = False

                    # Iterate over each on the ingresses
                    for ingresses in groups.ingresses:

                        if self.debug:
                          print('ingresses: '+str(ingresses)+lineno())

                        if type(ingresses) == type(dict()):

                            if self.debug:
                                print('ingress is a dict'+lineno())

                            if IpAddr.ip4_cidr_range(ingresses,debug=self.debug)==True or IpAddr.ip6_cidr_range(ingresses,debug=self.debug):
                                if self.debug:
                                    print('ip4/6 address is /32 or /128' + lineno())

                            else:
                                if self.debug:
                                    print('ip4/6 address does not end with /32 or /128' + lineno())

                                if self.debug:
                                    print("\n\n##########################################################")
                                    print('Resource is not valid - appending to list')
                                    print('logical resource id: ' + str(groups.logical_resource_id) + lineno())
                                    print("#############################################################\n")
                                logical_resource_ids.append(str(groups.logical_resource_id))

                        elif type(ingresses) == type(list()):

                            if self.debug:
                                print("ingress is a list() "+lineno())

                            for item in ingresses:

                                if IpAddr.ip4_cidr_range(item,debug=self.debug):
                                    if self.debug:
                                        print('ip4/6 address is /32 or /128' + lineno())
                                    continue

                                if IpAddr.ip6_cidr_range(item,debug=self.debug):
                                    if self.debug:
                                        print('ip4/6 address is /32 or /128' + lineno())
                                    continue

                            if self.debug:
                                print("\n\n##########################################################")
                                print('Resource is not valid - appending to list')
                                print('logical resource id: ' + str(groups.logical_resource_id) + lineno())
                                print("#############################################################\n")
                            logical_resource_ids.append(str(groups.logical_resource_id))

                        else:

                            if self.debug:
                                print('vars: '+str(vars(ingresses))+lineno())
                                print('ingress is not a list or dict'+lineno())

                            if hasattr(ingresses, 'cidrIp'):
                                if self.debug:
                                    print('has cidrIp '+lineno())

                                if IpAddr.ip4_cidr_range(ingresses,debug=self.debug):

                                    if self.debug:
                                        print('ip4/6 address is /32 or /128' + lineno())

                                    continue

                            if hasattr(ingresses,'cidrIpv6'):

                                if self.debug:
                                    print('ip4/6 address is /32 or /128'+lineno())

                                if IpAddr.ip6_cidr_range(ingresses, debug=self.debug):
                                    if self.debug:
                                        print('ip4/6 address is /32 or /128' + lineno())

                                continue

                            if not hasattr(ingresses,'cidrIp') and not hasattr(ingresses,'cidrIpv6'):
                                if self.debug:
                                    print('does not have a cidr entry')
                                continue

                            if self.debug:
                                print("\n\n##########################################################")
                                print('Resource is not valid - appending to list')
                                print('logical resource id: ' + str(groups.logical_resource_id) + lineno())
                                print("#############################################################\n")
                            logical_resource_ids.append(str(groups.logical_resource_id))
            else:
              sys.exit(1)

        if self.debug:
            print('violations: '+str(list(set(logical_resource_ids)))+lineno())

        if self.debug:
            print('Getting all the standalone ingress resources')

        standalone_resources= self.cfn_model.standalone_ingress()

        # iterate over the routes
        for resource in standalone_resources:

            if self.debug:
                print("\n\n#########################################")
                print('standalone resource: ' + str(resource) + lineno())
                print('vars: ' + str(vars(resource)) + lineno())
                print('type: '+str(type(resource))+lineno())
                print("############################################\n")

            if hasattr(resource,'cidrIp'):

                if self.debug:
                    print('has cidrIp attributes'+lineno())

                if IpAddr.ip4_cidr_range(resource.cidrIp,debug=self.debug):
                    if self.debug:
                        print('ip4/6 address is /32 or /128' + lineno())
                    continue

                else:
                    if self.debug:
                        print('ip4/6 address does not end with /32 or /128' + lineno())
                    logical_resource_ids.append(resource.logical_resource_id)

            if hasattr(resource,'cidrIpv6'):
                if self.debug:
                    print('has cidrIpv6 attributes' + lineno())

                if  IpAddr.ip6_cidr_range(resource.cidrIpv6,debug=self.debug):
                    if self.debug:
                        print('ip4/6 address is /32 or /128' + lineno())
                    continue

                else:
                    if self.debug:
                        print('ip4/6 address does not end with /32 or /128' + lineno())
                    logical_resource_ids.append(resource.logical_resource_id)

        if self.debug:
            print('violations: '+str(list(set(logical_resource_ids)))+lineno())

        return logical_resource_ids