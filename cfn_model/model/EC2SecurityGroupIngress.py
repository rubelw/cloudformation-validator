from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class EC2SecurityGroupIngress(ModelElement):
    """
    Ec2 security group ingress model
    """
    def __init__(self, cfn_model, debug=False):
        """
        Initialize
        :param cfn_model: 
        :param debug: 
        """
        self.debug = debug

        if self.debug:
            print('EC2SecurityGroupIngress __init__')
        ModelElement.__init__(self, cfn_model)

        self.resource_type = 'AWS::EC2::SecurityGroupIngress'