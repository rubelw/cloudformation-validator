from __future__ import absolute_import, division, print_function
import inspect
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' - RuleDefinition - line number: '+str(inspect.currentframe().f_back.f_lineno))


class RuleDefinition:
    """
    Rule definition
    """

    def __init__(self, id, type,message, debug=False):
        """
        Initialize RuleDefinition
        :param id: 
        :param type: 
        :param message: 
        :param debug: 
        """
        self.id = id
        self.type = type
        self.message = message
        self.debug= debug

        if self.debug:
            print('RuleDefinition - init'+lineno())
            print('id: '+str(id)+lineno())
            print('type: '+str(type)+lineno())
            print('message: '+str(message)+lineno())
            print('debug: '+str(debug)+lineno())

    def to_string(self):
        """
        Convert rule definition to a string
        :return: 
        """
        if self.debug:
            print('to_string'+lineno())

        return "id: "+str(self.id)+", type: "+str(self.type)+", message: "+str(self.message)

    def to_hash(self):
        """
        Convert RuleDefinition to a hash
        :return: 
        """
        if self.debug:
            print('to_hash'+lineno())
            print('id: '+str(self.id)+lineno())

        data = {
            'id': str(self.id),
            'type': str(self.type),
            'message': str(self.message)
        }

        return data


