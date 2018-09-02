from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)


def lineno():
    """Returns the current line number in our program."""
    return str(' - References - line number: '+str(inspect.currentframe().f_back.f_lineno))



class References:
    """
    References model
    """
    
    @staticmethod
    def resolve_value(cfn_model, value, debug=False):
        """
        ???
        :param value:
        :param debug:
        :return:
        """
        if debug:
            print('resolve_value'+lineno())
            print('value: '+str(value)+lineno())

        if type(value) == type(dict()):

            if 'Ref' in value:
                ref_id = value['Ref']

                if sys.version_info[0] < 3:
                    if type(ref_id) == type(unicode()):
                        if str(ref_id) in cfn_model.parameters:
                            return value
                            # return value if cfn_model.parameters[ref_id].synthesized_value.nil?
                            # return cfn_model.parameters[ref_id].synthesized_value
                        else:
                           return value
                    else:
                      return value

                else:
                    if type(ref_id) == type(str()):
                        if debug:
                            print('ref id is a string '+lineno())
                            print('params: '+str(cfn_model))
                        if str(ref_id) in cfn_model.parameters:
                            if debug:
                                print('ref id in parameters - id is: '+str(ref_id)+lineno())
                                print('returning: '+str(value))
                            return value
                            # return value if cfn_model.parameters[ref_id].synthesized_value.nil?
                            # return cfn_model.parameters[ref_id].synthesized_value
                        else:
                           return value
                    else:
                      return value
            else:
                return value
        else:
          return value

    @staticmethod
    def is_security_group_id_external(group_id, debug=False):
        """
        Is security group id external
        :param debug:
        :return:
        """
        if debug:
            print('\n#####################################################')
            print('Checking if security group id is external')
            print('is_security_group_id_external'+lineno())
            print('group_id: '+str(group_id)+lineno())
            print("######################################################\n")

        if group_id:
            id = References.resolve_security_group_id(group_id,debug=debug)

            if id:
                return id
            else:
                return None

        return False

    @staticmethod
    def resolve_security_group_id(group_id, debug=False):
        """
        Resolve security group id
        :param debug:
        :return:
        """
        if debug:
            print("\n\n##########################################")
            print('resolve_security_group id'+lineno())
            print('group_id: '+str(group_id)+lineno())
            print("##############################################\n")

        if group_id:
            if debug:
                print('there is a group id'+lineno())

            if sys.version_info[0] < 3:

                if type(group_id) == type(unicode()):
                    if debug:
                        print('type is unicode' + lineno())

                return group_id

            elif type(group_id) == type(str()):
                if debug:
                    print('type is string'+lineno())

                return group_id


            elif type(group_id) == type(dict()):
                if debug:
                    print('type is dict'+lineno())
                    print('groupid '+str(group_id)+lineno())

                ## an imported value can only yield a literal to an external sg vs. referencing something local
                if 'Ref' in group_id:
                    if debug:
                        print('returning '+str(group_id['Ref'])+lineno())
                    return group_id['Ref']

                elif 'Fn::GetAtt' in group_id:
                    return References.logical_resource_id_from_get_att(group_id['Fn::GetAtt'])
                else:
                    # anything else will be string manipulation functions
                    # which again leads us back to a string which must be an external security group known out of band
                    # so don't/can't link it up to a security group
                    return None

            else:
                if debug:
                    print('type is not a string'+lineno())
                return None
        else:
            return None

    @staticmethod
    def logical_resource_id_from_get_att(attribute_spec, debug=False):
        """
        ???
        :param debug:
        :return:
        """
        if debug:
            print('logical_resource_id_from_get_att'+lineno())
            print('attribute_spec: '+str(attribute_spec)+lineno())

        if type(attribute_spec) == type(list()):
            if attribute_spec[1] == 'GroupId':
                return attribute_spec[0]
            else:
                # this could be a reference to a nested stack output so treat it as external
                # and presume the ingress is freestanding.
                return None
        elif type(attribute_spec) == type(str()) or type(attribute_spec) == type(unicode()):
            attributes = attribute_spec.split('.')

            if attributes[1] == 'GroupId':
                return attributes[0]
            else:
                # this could be a reference to a nested stack output so treat it as external
                # and presume the ingress is freestanding.
                return None