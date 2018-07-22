from cfn_model.model.ModelElement import ModelElement



class EC2Instance(ModelElement):

    def __init__(self, cfn_model):
        '''
        Initialize
        :param cfn_model: 
        '''
        # attr_accessor :security_groups
        ModelElement.__init__(self, cfn_model)

        self.securityGroupIds= []
        self.networkInterfaces= []
        self.security_groups= []
        self.resource_type = 'AWS::EC2::Instance'



