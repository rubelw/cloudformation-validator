from cfn_model.model.ModelElement import ModelElement

class SNSTopicPolicy(ModelElement):

    _cfn_model = None

    def __init__(self, cfn_model):
        '''
        Initialize
        :param cfn_model:
        '''

        ModelElement.__init__(self, cfn_model)

        self._topics = []
        self.policy_document = None
        self._resource_type = 'AWS::SNS::TopicPolicy'


