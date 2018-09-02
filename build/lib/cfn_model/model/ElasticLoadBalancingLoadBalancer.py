from __future__ import absolute_import, division, print_function
from cfn_model.model.ModelElement import ModelElement


class ElasticLoadBalancingLoadBalancer(ModelElement):
    """
    Elastic load balance load balancer model
    """
    def __init__(self, cfn_model):
        """
        Initialize
        :param cfn_model: 
        """
        ModelElement.__init__(self, cfn_model)

        self.securityGroups = []
        self.security_groups = []
        self.subnets = []
        self.tags = []
        self.availabilityZones = []
        self.instances = []
        self.appCookieStickinessPolicy = []
        self.lBCookieStickinessPolicy = []
        self.policies = []
        self.listeners = []
        self.accessLoggingPolicy={}
        self.resource_type = 'AWS::ElasticLoadBalancing::LoadBalancer'