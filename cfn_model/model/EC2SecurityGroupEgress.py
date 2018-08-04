from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class EC2SecurityGroupEgress(ModelElement):
    """
    Ec2 security group egress model
    """
    def __init__(self, cfn_model, debug=False):
        """
        Initialize
        :param cfn_model:
        :param debug:
        """
        self.debug = debug

        if self.debug:
            print('EC2SecurityGroupEgress __init__')

        ModelElement.__init__(self, cfn_model)

        self.resource_type = 'AWS::EC2::SecurityGroupEgress'



