from cfn_model.model.ModelElement import ModelElement


class IAMPolicy(ModelElement):

    def __init__(self, cfn_model):
        '''
        Initialize
        :param cfn_model: 
        '''
        ModelElement.__init__(self, cfn_model)

        self.groups= []
        self.roles= []
        self.users= []
        self.resource_type = 'AWS::IAM::Policy'



