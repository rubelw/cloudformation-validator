from __future__ import absolute_import, division, print_function
import inspect
import sys
import json
from cloudformation_validator.RuleDefinition import RuleDefinition
from collections import OrderedDict
from builtins import (str)



def lineno():
    """Returns the current line number in our program."""
    return str(' - Violation - line number: '+str(inspect.currentframe().f_back.f_lineno))



class Violation(RuleDefinition):

    def __init__(self, id, type, message, logical_resource_ids=None, debug=False):
        """
        Initialize Violation
        :param id: 
        :param type: 
        :param message: 
        :param logical_resource_ids: 
        :param debug: 
        """
        RuleDefinition.__init__(self, id, type, message)
        self.attr_reader = None
        self.message = message
        self.type = type
        self.logical_resource_ids= logical_resource_ids
        self.id=id
        self.debug = debug

        if self.debug:
            print('Violation - init'+lineno())


    def id(self):
        return self.id()

    def type(self):
        return self.type()

    def message(self):
        return self.message()

    def logical_resource_ids(self):
        return self.logical_resource_ids()

    def to_string(self):
        """
        Returns violation as a string
        :return: 
        """
        if self.debug:
            print('to string'+lineno())
        #FIXME
        sys.exit(1)
        #"#{super} #{@logical_resource_ids}"


    def to_hash(self):
        """
        Converts violation to hash
        :return: 
        """
        if self.debug:
            print('to hash'+lineno())
            print('logical resource ids: '+str(self.logical_resource_ids)+lineno())
            print('logical id type: '+str(type(self.logical_resource_ids))+lineno())
            print('message: '+str(self.message)+lineno())




        hash = {'id': self.id,'type':self.type ,'message': self.message, 'logical_resource_ids': str(self.logical_resource_ids)}

        order_of_keys = ["id", "type", "message","logical_resource_ids"]

        list_of_tuples = []
        for key in order_of_keys:
            if self.debug:
                print('key: '+str(key)+lineno())
                print('value: '+str(hash[key])+lineno())

            if str(key) == 'logical_resource_ids' and type(hash[key])== type(list()):
                if self.debug:
                    print('is a list: '+lineno())
                mylist = sorted(json.loads(str(hash[key]).replace("'",'"')))
                my_newlist = []
                for item in mylist:
                    my_newlist.append(str(item))

                list_of_tuples.append(tuple((key, str(my_newlist))))


            else:
                list_of_tuples.append(tuple((key, hash[key])))

        #list_of_tuples = [(key, hash[key]) for key in order_of_keys]
        new_results = OrderedDict(list_of_tuples)



        if self.debug:
            print('#####################################')
            print('hash is: '+str(new_results)+lineno())
            print('#####################################')

        return new_results

