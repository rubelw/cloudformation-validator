from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class EC2SecurityGroup(ModelElement):
    """
    Ec2 security group model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """

        ModelElement.__init__(self, cfn_model)
        self.securityGroupIngress = []
        self.securityGroupEgress = []
        self.ingresses = []
        self.egresses = []
        self.tags = []

        self.resource_type = 'AWS::EC2::SecurityGroup'