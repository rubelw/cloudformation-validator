from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class IAMGroup(ModelElement):
    """
    IAM group model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """
        ModelElement.__init__(self, cfn_model)

        self.managedPolicyArns= []
        self.policies= []
        self.policy_objects= []

        self.resource_type = 'AWS::IAM::Group'



