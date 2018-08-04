from __future__ import absolute_import, division, print_function
import inspect
import sys
from cloudformation_validator.RoleDefinition import RoleDefinition



def lineno():
    """Returns the current line number in our program."""
    return str(' - Policy - line number: '+str(inspect.currentframe().f_back.f_lineno))



class Policy(RoleDefinition):

    def __init__(self, id, type, message, logical_resource_ids=None, debug=False):
        '''
        Initialize Violation
        :param id: 
        :param type: 
        :param message: 
        :param logical_resource_ids: 
        :param debug: 
        '''
        RoleDefinition.__init__(self, id, type, message)
        self.attr_reader = None
        self.message = message
        self.type = type
        self.logical_resource_ids= logical_resource_ids
        self.id=id
        self.debug = debug

        if self.debug:
            print('Violation - init'+lineno())


    def to_string(self):
        '''
        Returns violation as a string
        :return: 
        '''
        if self.debug:
            print('to string'+lineno())
        #FIXME
        sys.exit(1)
        #"#{super} #{@logical_resource_ids}"


    def to_hash(self):
        '''
        Converts violation to hash
        :return: 
        '''
        if self.debug:
            print('to hash'+lineno())
            print('logical id type: '+str(type(self.logical_resource_ids))+lineno())
            print('message: '+str(self.message))

        hash = {'id': self.id,'type':self.type ,'message': self.message, 'logical_resource_ids': self.logical_resource_ids}

        if self.debug:
            print('hash is: '+str(hash)+lineno())

        return hash