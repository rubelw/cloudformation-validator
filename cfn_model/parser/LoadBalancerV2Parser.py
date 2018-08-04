from __future__ import absolute_import, division, print_function
import inspect
import sys


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

        if self.debug:
            print('parse'+lineno())
        # FIXME
        sys.exit(1)
        #load_balancer = resource

        ##could be a List<Subnet::Id>
        ## if load_balancer.subnets.size < 2
        ##   raise ParserError.new("Load Balancer must have at least two subnets: #{load_balancer.logical_resource_id}")
        ## end

        #if load_balancer.securityGroups.is_a? Array
        #  load_balancer.security_groups = load_balancer.securityGroups.map do |security_group_reference|
        #    cfn_model.find_security_group_by_group_id(security_group_reference)
        #  end
        #else
          # er... list of ids or comma separated list.  just punt.
        #  load_balancer.security_groups = []
        #end
        #load_balancer
