from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class SQSQueuePolicy(ModelElement):
    """
    SQS Queue Policy Model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """

        ModelElement.__init__(self, cfn_model)

        self.queues= []
        self.policy_document = None
        self.resource_type = 'AWS::SQS::QueuePolicy'