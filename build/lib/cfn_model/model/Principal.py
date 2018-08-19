from __future__ import absolute_import, division, print_function
import inspect
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' - Principal - line number: '+str(inspect.currentframe().f_back.f_lineno))


class Principal:
    """
    Principal model
    """
    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        self.debug = debug

        if self.debug:
            print('__init__'+lineno())

    def wildcard(self, principal):
        """
        Whether principal has a wildcard
        :param principal: 
        :return: 
        """
        if self.debug:
            print('wildcard'+lineno())

            print('principal: '+str(principal)+lineno())
            print('type: '+str(type(principal))+lineno())

        if sys.version_info[0] < 3:
            if type(principal) == type(unicode()):
                return self.has_asterisk(principal)
            elif type(principal) == type(dict()):

                for value in principal:
                    if self.debug:
                        print('value type: ' + str(type(value)) + lineno())
                        print('key: ' + str(value) + lineno())
                        print('value: ' + str(principal[value]) + lineno())

                    if type(value) == type(str()) or type(value) == type(unicode()):
                        if self.has_asterisk(principal[value]):
                            return True

                    elif type(value) == type(list()):
                        for item in value:

                            if self.has_asterisk(item):
                                return True
            return False
        else:
            if type(principal) == type(str()):
                return self.has_asterisk(principal)

            elif type(principal) == type(dict()):

                for value in principal:
                    if self.debug:
                        print('value type: '+str(type(value))+lineno())
                        print('key: '+str(value)+lineno())
                        print('value: '+str(principal[value])+lineno())

                    if type(value) == type(str()) or type(value) == type(unicode()):
                        if self.has_asterisk(principal[value]):
                            return True

                    elif type(value)== type(list()):
                        for item in value:

                            if self.has_asterisk(item):
                                return True
            return False

    def has_asterisk(self, string):
        """
        Whether string has asterisk
        :param string: 
        :return: 
        """
        if self.debug:
            print('has asterisk'+lineno())

        if '*' in string:
            if self.debug:
                print('has an asterisk '+lineno())

            return True

        return False