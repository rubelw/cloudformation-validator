from __future__ import absolute_import, division, print_function
import copy
import sys
import inspect
import re
import sys
from cfn_model.model.EC2SecurityGroupIngress import EC2SecurityGroupIngress
from cfn_model.model.EC2SecurityGroupEgress import EC2SecurityGroupEgress
from cfn_model.model.References import References
from builtins import (str)


def lineno():
    """Returns the current line number in our program."""
    return str(' -  SecurityGroupParser- line number: '+str(inspect.currentframe().f_back.f_lineno))

class SecurityGroupParser:
    """
    Security group parser
    """
    
    @staticmethod
    def parse(cfn_model, resource, debug=False):
        """
        Parse security group
        :param resource:
        :param debug:
        :return:
        """
        if debug:
            print('parse'+lineno())

        security_group = copy.copy(resource)
        security_group = SecurityGroupParser.objectify_egress(cfn_model, security_group, debug=debug)
        security_group = SecurityGroupParser.objectify_ingress(cfn_model, security_group, debug=debug)

        if debug:
            print('objectified egress'+lineno())

        security_group = SecurityGroupParser.wire_ingress_rules_to_security_group(cfn_model, security_group, debug=debug)
        security_group = SecurityGroupParser.wire_egress_rules_to_security_group(cfn_model, security_group, debug=debug)

        return security_group

    @staticmethod
    def objectify_ingress(cfn_model, security_group, debug=False):
        """
        Objectivy ingress statment
        :param security_group:
        :param debug:
        :return:
        """
        if debug:
            print("\n\n#########################")
            print('objectify_ingress'+lineno())

        if security_group:
            if debug:
                print('there is a security group'+lineno())
                print('security group: '+str(security_group)+lineno())
                print('type: '+str(type(security_group))+lineno())
                print('vars: '+str(vars(security_group))+lineno())
                print('###########################\n\n')

            if 'Properties' in security_group.cfn_model:

                if debug:
                    print('there are properties in the security group cfn model'+lineno())

                # If there is a ingress in properties
                if 'SecurityGroupIngress' in security_group.cfn_model['Properties']:

                    if debug:
                        print('has securitygroupingress property'+lineno())
                        print('type: '+str(type(security_group.cfn_model['Properties']['SecurityGroupIngress']))+lineno())

                    # if the ingress is a list
                    if type(security_group.cfn_model['Properties']['SecurityGroupIngress']) == type(list()):
                        if debug:
                            print('is a list'+lineno())

                        if debug:
                            print('Iterating over each list in array'+lineno())
                        # Iterate over each sg in array
                        for sg in security_group.cfn_model['Properties']['SecurityGroupIngress']:
                            if debug:
                                print(str(sg)+lineno())

                            ingress_object = EC2SecurityGroupIngress(cfn_model,debug=debug)
                            ingress_object.logical_resource_id = security_group.logical_resource_id

                            for key in sg:
                                if debug:
                                    print('key: '+str(key)+lineno())
                                    print('value: '+str(sg[key])+lineno())

                                if '::' in key:
                                    if debug:
                                        print(':: in key'+lineno())
                                    continue
                                else:
                                    if debug:
                                        print(':: not in key '+lineno())
                                    new_key_name = SecurityGroupParser.initialLower(key)

                                    if debug:
                                        print('new key name: '+str(new_key_name)+lineno())
                                    setattr(ingress_object,SecurityGroupParser.initialLower(key),sg[key])

                            if debug:
                                print(str(vars(ingress_object))+lineno())

                            security_group.ingresses.append(ingress_object)

                        if debug:
                            print('Done iterating of list - returning security group to caller '+lineno())

                        return security_group

                    # If the ingress routes is a dictionary
                    elif type(security_group.cfn_model['Properties']['SecurityGroupIngress']) == type(dict()):
                        if debug:
                            print('is a dict'+lineno())
                            print(str(security_group.cfn_model['Properties']['SecurityGroupIngress'])+lineno())


                        ingress_object = EC2SecurityGroupIngress(cfn_model)
                        ingress_object.logical_resource_id = security_group.logical_resource_id

                        # Iterate over each key-value pair in dictionary and associate
                        # to an object attribute
                        for key in security_group.cfn_model['Properties']['SecurityGroupIngress']:
                            if debug:
                                print('key: ' + str(key) + lineno())
                                print('value: ' + str(security_group.cfn_model['Properties']['SecurityGroupIngress'][key]) + lineno())

                            setattr(ingress_object, SecurityGroupParser.initialLower(key), security_group.cfn_model['Properties']['SecurityGroupIngress'][key])

                        security_group.ingresses.append(ingress_object)
                        return security_group

                    # if the ingress is a list
                    else:
                        print('security group ingress is not a list or dict')
                        print(str('type: ')+str(type(security_group.cfn_model['Properties']['SecurityGroupIngress'])+lineno()))
                        sys.exit(1)

    @staticmethod
    def objectify_egress(cfn_model, security_group, debug=False):
        """
        Trying to convert a security group egress in to an egress object
        :param security_group:
        :param debug:
        :return:
        """
        if debug:
            print("\n\n###############")
            print('objectify_egress'+lineno())
            print('security group type: '+str(type(security_group))+lineno())
            print(str(vars(security_group))+lineno())
            print('##################\n\n')

        if security_group:
            if debug:
                print("\n\n#######################################")
                print('Details regarding security group')
                print('there is a security group'+lineno())
                print('security group: '+str(security_group)+lineno())
                print('vars: '+str(vars(security_group))+lineno())
                print("###########################################\n")

            if 'Properties' in security_group.cfn_model:

                if debug:
                    print('there are properties in the security group cfn model' + lineno())

                # If there is a egress property
                if 'SecurityGroupEgress' in security_group.cfn_model['Properties']:

                    if debug:
                        print('has securitygroupegress property'+lineno())
                        print('type: '+str(type(security_group.cfn_model['Properties']['SecurityGroupEgress']))+lineno())

                    # If the egress is an array
                    if type(security_group.cfn_model['Properties']['SecurityGroupEgress']) == type(list()):
                        if debug:
                            print('is a list'+lineno())

                        for sg in security_group.cfn_model['Properties']['SecurityGroupEgress']:
                            if debug:
                                print(str(sg)+lineno())

                            egress_object = EC2SecurityGroupEgress(cfn_model,debug=debug)
                            egress_object.logical_resource_id = security_group.logical_resource_id

                            for key in sg:
                                if debug:
                                    print('key: '+str(key)+lineno())
                                    print('value: '+str(sg[key])+lineno())

                                if '::' in key:
                                    continue

                                else:
                                    if debug:
                                        print(':: not in key '+lineno())
                                    new_key_name = SecurityGroupParser.initialLower(key)

                                    if debug:
                                        print('new key name: '+str(new_key_name)+lineno())

                                    setattr(egress_object,SecurityGroupParser.initialLower(key),sg[key])

                            if debug:
                                print(str(vars(egress_object))+lineno())

                        security_group.egresses.append(egress_object)

                        return security_group

                    # If the egress is a dictionary
                    elif type(security_group.cfn_model['Properties']['SecurityGroupEgress']) == type(dict()):

                        if debug:
                            print('is a dict'+lineno())
                            print(str(security_group.cfn_model['Properties']['SecurityGroupEgress'])+lineno())
                        # {'CidrIp': '10.1.2.3/32', 'FromPort': 34, 'ToPort': 36, 'IpProtocol': 'tcp'}

                        egress_object = EC2SecurityGroupIngress(cfn_model)
                        egress_object.logical_resource_id = security_group.logical_resource_id

                        # Iterate over each key-value pair in the dictionary and create
                        # an object attribute
                        for key in security_group.cfn_model['Properties']['SecurityGroupEgress']:
                            if debug:
                                print('key: ' + str(key) + lineno())
                                print('value: ' + str(security_group.cfn_model['Properties']['SecurityGroupEgress'][key]) + lineno())

                            matchObj = re.match(r'::', key, re.M | re.I)

                            if matchObj:
                                if debug:
                                    print("matchObj.group() : ", matchObj.group() + lineno())
                                continue
                            else:
                                if debug:
                                    print("No match!!" + lineno())

                                setattr(egress_object, SecurityGroupParser.initialLower(key), security_group.cfn_model['Properties']['SecurityGroupEgress'][key])

                        if debug:
                            print(str(vars(egress_object)) + lineno())

                        security_group.egresses.append(egress_object)
                        return security_group

                    else:
                        print("\n#############################")
                        print('Security group is not egress')
                        print("################################\n")

            else:

                if debug:
                    print('no properties in security group'+lineno())

        else:
            if debug:
                print('no security group'+lineno())

        return security_group

    @staticmethod
    def initialLower(key_name):
        """
        First character to lower case
        :return:
        """
        first_character = str(key_name)[:1]
        remaining_characters = str(key_name)[1:]
        new_property_name = str(first_character.lower()) + str(remaining_characters)

        return new_property_name

    @staticmethod
    def wire_ingress_rules_to_security_group(cfn_model, security_group, debug=False):
        """
        Wires a standalone ingress rule to a security group
        :param security_group:
        :param debug:
        :return:
        """
        if debug:
            print("\n\n###############")
            print('wire_ingress_rules_to_security_group'+lineno())
            print('##################\n\n')

            print('sg: '+str(security_group)+lineno())
            print('cfn_model: '+str(cfn_model)+lineno())
            print('vars: '+str(vars(cfn_model))+lineno())

        if not security_group:
            return security_group

        # Get all the EC2::SecurityGroupIngress resources
        ingress_rules = cfn_model.resources_by_type('AWS::EC2::SecurityGroupIngress')

        # Iterate over each of the ingress resources
        for security_group_ingress in ingress_rules:

            if debug:
                print("\n\n###########################################################")
                print('Standalone ingress resource')
                print('security_group_ingress: '+str(security_group_ingress)+lineno())
                print('vars: '+str(vars(security_group_ingress))+lineno())
                print('dirs: '+str(dir(security_group_ingress))+lineno())
                print("##############################################################\n")

            if 'Properties' in security_group_ingress.cfn_model:
                if debug:
                    print('security group ingress cfn model has properties'+lineno())
                if 'GroupId' in security_group_ingress.cfn_model['Properties']:
                    if debug:
                        print('security group ingress has groupid '+str(security_group_ingress.cfn_model['Properties']['GroupId'])+lineno())

                    group_id = References.resolve_security_group_id(security_group_ingress.cfn_model['Properties']['GroupId'],debug=debug)
                    if debug:
                        print('group id: '+str(group_id)+lineno())
                        print('security group logical resource id: '+str(security_group_ingress.logical_resource_id)+lineno())

                    # standalone ingress rules are legal - referencing an external security group
                    if not group_id:
                        continue

                    # If the group id in the standalone ingress matches the logical resource id
                    # of the actual security group
                    if security_group.logical_resource_id == group_id:

                        if debug:
                            print('security group logical resourceid and group id are equal'+lineno())

                        if not hasattr(security_group,'ingresses'):
                            print('security group does not have ingresses array attribute'+lineno())
                            print('vars: '+str(security_group_ingress))
                            sys.exit(1)
                        else:
                            security_group.ingresses.append(security_group_ingress)

                else:
                    print('Security group ingress has no groupid')
                    sys.exit(1)

        if debug:
            print('done wiring_ingress_rules_to_security_group '+lineno())

        return security_group

    @staticmethod
    def wire_egress_rules_to_security_group(cfn_model, security_group, debug=False):
        """
        Wire egress rule to a security group
        :param security_group:
        :param debug:
        :return:
        """
        if debug:
            print("\n\n###############")
            print('wire_egress_rules_to_security_group'+lineno())
            print('##################\n\n')
            print('sg: '+str(security_group)+lineno())
            print('cfn_model: '+str(cfn_model)+lineno())
            print('vars: '+str(vars(cfn_model))+lineno())

        if not security_group:
            return security_group

        egress_rules = cfn_model.resources_by_type('AWS::EC2::SecurityGroupEgress')

        # Iterate over each of the egress resources
        for security_group_egress in egress_rules:

            if debug:
                print("\n\n###########################################################")
                print('Standalone ingress resource')
                print('security_group_ingress: '+str(security_group_egress)+lineno())
                print('vars: '+str(vars(security_group_egress))+lineno())
                print('dirs: '+str(dir(security_group_egress))+lineno())
                print("##############################################################\n")

            if 'Properties' in security_group_egress.cfn_model:
                print('security group egress cfn model has properties'+lineno())
                if 'GroupId' in security_group_egress.cfn_model['Properties']:
                    print('security group ingress has groupid '+str(security_group_egress.cfn_model['Properties']['GroupId'])+lineno())

                    group_id = References.resolve_security_group_id(security_group_egress.cfn_model['Properties']['GroupId'],debug=debug)
                    if debug:
                        print('group id: '+str(group_id)+lineno())
                        print('security group logical resource id: '+str(security_group_egress.logical_resource_id)+lineno())

                    # standalone egress rules are legal - referencing an external security group
                    if not group_id:
                        continue

                    # If the group id in the standalone egress matches the logical resource id
                    # of the actual security group
                    if security_group.logical_resource_id == group_id:

                        if debug:
                            print('security group logical resourceid and group id are equal'+lineno())

                        if not hasattr(security_group,'egresses'):
                            print('security group does not have egresses array attribute'+lineno())
                            print('vars: '+str(security_group_egress))
                            sys.exit(1)
                        else:
                            security_group.egresses.append(security_group_egress)

        return security_group