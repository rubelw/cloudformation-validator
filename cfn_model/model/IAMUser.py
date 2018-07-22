from cfn_model.model.ModelElement import ModelElement


class IAMUser(ModelElement):

    def __init__(self, cfn_model):
        '''
        Initialize
        :param cfn_model: 
        '''
        ModelElement.__init__(self, cfn_model)
        self.policies = []
        self.policy_objects=[]
        self.group_names = []
        self.groups=[]
        self.resource_type = 'AWS::IAM::User'