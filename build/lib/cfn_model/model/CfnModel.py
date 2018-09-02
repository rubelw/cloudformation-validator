from __future__ import absolute_import, division, print_function
import copy
import inspect
from builtins import (str)
from cfn_model.model.References import References
from cfn_model.model.Parameter import Parameter


def lineno():
    """Returns the current line number in our program."""
    return str(' - CfnModel - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


class CfnModel:
    """
    Cloudformation model
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        # attr_accessor :raw_model
        self.parameters={}
        self.resources = {}
        self.raw_model = None
        self.debug = debug
        if self.debug:
            print('CfnModel - init'+lineno())

    def copy(self):
        """
        copy the model
        :return: copy of model
        """
        if self.debug:
            print('CfnModel - copy'+lineno())

        return copy.copy(self.raw_model)

    def security_groups(self):
        """
        Get security groups
        :return: 
        """
        if self.debug:
            print("\n\n################################################################")
            print('CfnModel - security_groups - getting security group resources'+lineno())
            print("####################################################################\n")

        return self.resources_by_type('AWS::EC2::SecurityGroup')

    def iam_users(self):
        """
        Get iam users
        :return: 
        """
        if self.debug:
            print("\n\n################################################################")
            print('CfnModel - iam_users - getting iam users resources'+lineno())
            print("####################################################################\n")

        return self.resources_by_type('AWS::IAM::User')

    def standalone_ingress(self):
        """
        Get standalone ingress resources
        :return: 
        """
        if self.debug:
            print("\n\n################################################################")
            print('CfnModel - standalone_ingress - getting security group ingress resources'+lineno())
            print("####################################################################\n")

        security_group_ingresses = []

        resources = self.resources_by_type('AWS::EC2::SecurityGroupIngress')

        for resource in resources:
            if self.debug:
                print("\n\n#############################################")
                print('Stand alone ingress'+lineno())
                print(str(resource) + lineno())
                print("################################################\n")

            if 'Properties' in resource.cfn_model:
                if self.debug:
                    print('properties in cfn_model: '+lineno())
                if 'GroupId' in resource.cfn_model['Properties']:
                    if self.debug:
                        print('groupid in properties: '+lineno())

                    if References.is_security_group_id_external(str(resource.cfn_model['Properties']['GroupId']) ,debug=self.debug):
                        security_group_ingresses.append(resource)
        if self.debug:
            print("\n############################################")
            print('These are the standalone security_group_ingresses: '+str(security_group_ingresses)+lineno())
            print("##############################################\n")

        return security_group_ingresses

    def standalone_egress(self):
        """
        Get standalone egress resources
        :return: 
        """
        if self.debug:
            print("\n\n################################################################")
            print('CfnModel - standalone_egress - getting security group egress resources'+lineno())
            print("####################################################################\n")

        security_group_egresses = []

        resources = self.resources_by_type('AWS::EC2::SecurityGroupEgress')

        for resource in resources:
            if self.debug:
                print(str(resource) + lineno())

            if 'Properties' in resource.cfn_model:

                if self.debug:
                    print('Properties in cfn_model '+lineno())

                if 'GroupId' in resource.cfn_model['Properties']:
                    if self.debug:
                        print('GroupId in properties'+lineno())

                    if References.is_security_group_id_external(
                            resource.cfn_model['Properties']['GroupId'],
                            debug=self.debug):

                        security_group_egresses.append(resource)

                if 'groupId' in resource.cfn_model['Properties']:
                    if self.debug:
                        print('groupId in properties'+lineno())

                    if References.is_security_group_id_external(
                            resource.cfn_model['Properties']['groupId'],
                            debug=self.debug):

                        security_group_egresses.append(resource)

        if self.debug:
            print('security_group_egresses: '+str(security_group_egresses)+lineno())

        return security_group_egresses

    def resources_by_type(self, resource_type):
        """
        Get cfn resources by type
        :param resource_type: 
        :return: 
        """
        if self.debug:

            print('CfnModel - resource_by_type'+lineno())
            print("\n\n####################################")
            print('#### Looking for resource_type: '+str(resource_type)+' in raw_model'+lineno())
            print("####################################\n\n")

        resources = []

        if self.debug:
            print(str(self.resources)+lineno())

        # Iterating through the resources in the raw_model
        for resource in self.resources:
            if self.debug:
                print('resource: '+str(resource)+lineno())
                print('resource object: '+str(self.resources[resource])+lineno())

                print('type: '+str(self.resources[resource].resource_type)+lineno())
                print('vars: '+str(vars(self.resources[resource]))+lineno())
                print('resource type is: '+str(self.resources[resource].resource_type)+lineno())

            if str(self.resources[resource].resource_type) == str(resource_type):
                if self.debug:
                    print(' ### FOUND MATCHING RESOURCE TYPE '+lineno())

                resources.append(self.resources[resource])

        if self.debug:
            print('CfnModel - resources_by_type - returning resource'+lineno())

        if len(resources)<1:
            if self.debug:
                print('### Could not find matching type for: '+str(resource_type)+lineno())
        else:
            if self.debug:
                print("\n\n########################################")
                print('### found '+str(len(resources))+' '+str(resource_type)+' resources'+lineno())
                print("########################################\n\n")

        return resources

    def find_security_group_by_group_id(self, security_group_reference):
        """
        Get security group by security group id
        :param security_group_reference: 
        :return: 
        """
        if self.debug:
            print('CfnModel - find_security_group_by_group_id'+lineno())
            print('security_group_reference: '+str(security_group_reference)+lineno())

        security_group_id = References.resolve_security_group_id(security_group_reference)

        if not security_group_id:
            # # leave it alone since external ref or something we don't grok
            return security_group_reference
        else:

            security_groups = self.security_groups()

            for sg in security_groups:
                if self.debug:
                    print('sg: '+str(sg)+lineno())
                    print('vars: '+str(vars(sg))+lineno())

                if sg.logical_resource_id == sg:
                    return sg

            # leave it alone since external ref or something we don't grok
            return security_group_reference

    def transform_hash_into_parameters(self, cfn_hash):
        """
        Transform hash into parameters
        :param cfn_hash:
        :return:
        """

        if self.debug:
            print('CfnParser - transform_hash_into_parameters'+lineno())
            print('cfn_hash: '+str(cfn_hash)+lineno())


        if 'Parameters' in cfn_hash:

            for param in cfn_hash['Parameters']:

                if self.debug:
                    print(param+lineno())
                    print(str(cfn_hash['Parameters'][param])+lineno())

                parameter = Parameter(debug=self.debug)
                parameter.id = param
                parameter.type = cfn_hash['Parameters'][param]['Type']

                parameter.instance_variables.append(param+'='+cfn_hash['Parameters'][param]['Type'].lower().replace('-','_'))

                self.parameters[param] = parameter

