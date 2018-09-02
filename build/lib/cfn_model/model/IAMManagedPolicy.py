from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class IAMManagedPolicy(ModelElement):

    """
    IAM managed policy model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """
        ModelElement.__init__(self,cfn_model)

        self.groups = []
        self.roles = []
        self.users = []
        self.policy_document=None
        self.resource_type= 'AWS::IAM::ManagedPolicy'


    def policy_document(self, document):
        """
        Set the policy document
        :param document: 
        :return: 
        """
        self.policy_document=document
