from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class IAMRole(ModelElement):
    """
    IAM role model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """
        ModelElement.__init__(self, cfn_model)

        self.policies= []
        self.managedPolicyArns= []
        self.policy_objects = []
        self.assume_role_policy_document=None
        self.resource_type = 'AWS::IAM::Role'



