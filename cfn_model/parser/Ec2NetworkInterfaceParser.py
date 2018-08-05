from __future__ import absolute_import, division, print_function
import inspect
import sys

def lineno():
    """Returns the current line number in our program."""
    return str(' -  Ec2NetworkInterfaceParser- line number: '+str(inspect.currentframe().f_back.f_lineno))


class Ec2NetworkInterfaceParser:
    """
    Ec2 network interface parser
    """
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        print('Ec2NetworkInterfaceParser - parse'+lineno())
        # FIXME
        sys.exit(1)
    #network_interface = resource

    #if network_interface.groupSet.is_a? Array
    #  network_interface.security_groups = network_interface.groupSet.map do |security_group_reference|
    #    cfn_model.find_security_group_by_group_id(security_group_reference)
    #  end
    #else
    #  network_interface.security_groups = []
    #end

    #network_interface