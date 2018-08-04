from __future__ import absolute_import, division, print_function
import inspect
import copy
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' -  LoadBalancerParser- line number: '+str(inspect.currentframe().f_back.f_lineno))


class LoadBalancerParser:
    """
    Loadbalancer parser
    """
    
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse load balancer
        :param resource: 
        :param debug: 
        :return: 
        """
        if debug:
            print('parse'+lineno())

        load_balancer = copy.copy(resource)

        if debug:
            print('load_balancer'+str(vars(load_balancer))+lineno())
        if type(load_balancer) == type(list()):
            if debug:
                print('load_balancer is list')
            if hasattr(load_balancer,'securityGroups'):
                for sgs in load_balancer.securitygroups:
                    if debug:
                        print(sgs)
                    # FIXME
                    #cfn_model.find_security_group_by_group_id(security_group_reference
                    sys.exit(1)
        else:
            if debug:
                print('load_balancer is not a list'+lineno())
            load_balancer.security_groups= []
            
        return load_balancer