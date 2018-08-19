from __future__ import absolute_import, division, print_function
import inspect
import sys
from cfn_model.parser.ParserError import ParserError


def lineno():
    """Returns the current line number in our program."""
    return str(' -  LoadBalancerV2Parser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class LoadBalancerV2Parser:
    """
    Load balancer v2 parser
    """
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse load balancer v2
        :param resource: 
        :param debug: 
        :return: 
        """

        if debug:
            print('parse'+lineno())
            print('resource: '+str(resource))
            print('subnects: '+str(resource.subnets))

        if resource.subnets and len(resource.subnets)<2:

            try:
                raise ParserError('"Load Balancer must have at least two subnets:'+str(resource.subnets), None,debug=self.debug)
            except ParserError as e:

                raise ParserError('"Load Balancer must have at least two subnets:'+str(resource.subnets), None,debug=self.debug)
            #    #sys.exit(exc)

        if type(resource.securityGroups) == type(list()):
            for sg in resource.securityGroups:
                cfn_model.find_security_group_by_group_id(sg)

        else:
            # er... list of ids or comma separated list.  just punt.
            resource.security_groups = []

        return resource

