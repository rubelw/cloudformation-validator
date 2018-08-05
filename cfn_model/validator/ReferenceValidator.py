from __future__ import absolute_import, division, print_function
import re
import sys
from builtins import (str)
from cfn_model.parser import ParserError
import inspect
from builtins import (str)

def lineno():
    """Returns the current line number in our program."""
    return str(' -  ReferenceValidator- line number: '+str(inspect.currentframe().f_back.f_lineno))


class ReferenceValidator:
    """
    Reference validator
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug:
        """

        self.debug=debug

        if self.debug:

            print("\n\n#############################################")
            print('Creating ReferenceValidator - __init__'+lineno())
            print("################################################\n\n")

    def unresolved_references(self, cloudformation_hash):
        """
        Iterate over the cloudformation template
        :param cloudformation_hash:
        :return:
        """
        if self.debug:
            print("\n\n#################################################")
            print('ReferenceValidator - finding unresolved_references'+lineno())
            print("####################################################\n\n")

        if 'Parameters' in cloudformation_hash:
            if self.debug:
                print('There are parameters in the cloudformation template'+lineno())

            parameter_keys = []
            for key in cloudformation_hash['Parameters']:
                parameter_keys.append(key)
        else:
            parameter_keys = []

        if self.debug:
            print('parameter keys are: '+str(parameter_keys)+lineno())

        resource_keys = list(cloudformation_hash['Resources'].keys())

        if self.debug:
            print('resource keys are: '+str(resource_keys)+lineno())

            print("\n\n#####################################")
            print("Trying to find missing refs"+lineno())
            print("#########################################\n")

        new_list = parameter_keys + resource_keys

        missing_refs = self.all_references(cloudformation_hash)

        if self.debug:
            print('new_list: '+str(new_list)+lineno())
            print('missing_refs: '+str(missing_refs)+lineno())

        for x in new_list:

            if self.debug:
                print(str(x)+lineno())
            if missing_refs:
                if x in missing_refs:

                    missing_refs.remove(x)

        if self.debug:
            print('missing_refs: '+str(missing_refs)+lineno())

        return missing_refs


    def all_references(self, cloudformation_hash):
        """
        Iterate over all resources in the cloudformation template

        :param cloudformation_hash:
        :return:
        """
        if self.debug:
            print("\n\n#############################################")
            print('ReferenceValidator - all_references'+lineno())
            print("###############################################\n")

        result = None

        for resource in cloudformation_hash['Resources']:

            if self.debug:
                print("\n\n###################################")
                print('resource: '+str(resource)+lineno())
                print("#######################################\n")

            if 'Properties' in cloudformation_hash['Resources'][resource]:
                if self.debug:
                    print('resource: '+str(resource)+' has properties'+lineno())


                result = self.all_ref(cloudformation_hash['Resources'][resource]['Properties'])
                if self.debug:
                    print('result = '+str(result)+lineno())
                result_att = self.all_get_att(cloudformation_hash['Resources'][resource]['Properties'])

                for item in result_att:
                    result.append(item)

                if self.debug:
                    print('result = '+str(result)+lineno())

            else:
                if self.debug:
                    print('resource: '+str(resource)+' has no properties'+lineno())

        return result

    def all_ref(self, properties_hash):
        """
        Iterate over all properites in a resource and get all reference
        :param properties_hash:
        :return:
        """
        if self.debug:
            print("\n\n##############################################")
            print('ReferenceValidator - all_ref'+lineno())
            print('properties_hash: '+str(properties_hash)+lineno())
            print("##################################################\n")

        refs = []

        for property in properties_hash:

            if self.debug:
                print("\n########################################################")
                print('property hash: '+str(properties_hash[property])+lineno())
                print('data type: '+str(type(properties_hash[property]))+lineno())
                print('property: '+str(property)+lineno())
                print('value: '+str(properties_hash[property])+lineno())
                print("########################################################\n")

            if type(properties_hash[property]) == type(dict()):
                if self.debug:
                    print('property: '+str(property)+lineno())
                    print('value: '+str(properties_hash[property])+lineno())
                    print('subhash length: '+str(len(properties_hash[property]))+lineno())

                sub_hash = properties_hash[property]

                if len(sub_hash) == 1 and 'Ref' in sub_hash:
                    if self.debug:
                        print('subhash hash length of one and Ref key'+lineno())
                        print('subhash ref is: '+str(sub_hash['Ref'])+lineno())
                        print('subhash ref type is: '+str(type(sub_hash['Ref']))+lineno())

                    if type(sub_hash['Ref']) != type(str()) and type(sub_hash['Ref']) != type(unicode()):
                        raise ParserError.ParserError('Ref target must be string literal: ' + str(sub_hash['Ref']),debug=self.debug)

                    if not self.pseudo_reference(sub_hash['Ref']):
                        refs.append(sub_hash['Ref'])
                else:
                    if self.debug:
                        print('Trying to run all_refs again on subhash:'+str(sub_hash)+lineno())

                    new_refs = self.all_ref(sub_hash)
                    if self.debug:
                        print('new refs: '+str(new_refs)+lineno())

                    if new_refs:
                        refs.extend(new_refs)

        if self.debug:
            print('refs: '+str(list(set(refs)))+lineno())

        return list(set(refs))

    def all_get_att(self, properties_hash):
        """
        Iterate of all properties in hash
        :param properties_hash:
        :return:
        """
        if self.debug:
            print('ReferenceValidator - all_get_att'+lineno())
            print('properties_hash: '+str(properties_hash)+lineno())
        refs = ()

        if 'Properties' in properties_hash:
            if self.debug:
                print('properties hash ahs properties')

            # Iterating over all properties
            for property in properties_hash['Properties']:
                if self.debug:
                    print('property: '+str(property)+lineno())

                # If the property is a dictionary
                if type(properties_hash['Properties'][property])== type(dict()):
                    if self.debug:
                        print('property is dict: '+lineno())

                    sub_hash = properties_hash['Properties'][property]

                    # ! GetAtt too
                    if len(sub_hash)==1 and 'Fn::GetAtt' in sub_hash and sub_hash['Fn::GetAtt']==None:
                        if type(sub_hash['Fn::GetAtt']) == type(list()):
                            refs = refs + sub_hash['Fn::GetAtt'][0]
                        elif type(sub_hash['Fn::GetAtt']) == type(str()) or type(sub_hash['Fn::GetAtt']) == type(unicode()):
                            matchObj = re.match(r'([^.]*)\.(.*)', sub_hash['Fn::GetAtt'], re.M | re.I)

                            if matchObj:
                                if self.debug:
                                    print("matchObj.group() : ", matchObj.group())
                                    print("matchObj.group(1) : ", matchObj.group(1))
                                    print("matchObj.group(2) : ", matchObj.group(2))
                                refs = refs + matchObj.group(1)
                            else:
                                if self.debug:
                                    print("No match!!")
                    else:
                        refs = refs + self.all_get_att(sub_hash)
                else:
                    print('property is not a dictionary: '+lineno())
                    sys.exit(1)

        if self.debug:
            print('refs: '+str(refs)+lineno())

        return refs

    def pseudo_reference(self, ref):
        """
        Test whether the reference is a pseudo reference to AWS
        :param ref:
        :return:
        """
        if self.debug:
            print('ReferenceValidator - pseudo_reference')
            print('ref: '+str(ref))

        if 'AWS::' in ref:
            return True

        return False