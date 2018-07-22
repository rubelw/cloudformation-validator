import inspect
from cfn_model.parser.Error import Error



def lineno():
    """Returns the current line number in our program."""
    return str(' -  ParserError- line number: '+str(inspect.currentframe().f_back.f_lineno))


class ParserError(Error):

    def __init__(self,message, validation_errors=None, debug=False):
        '''
        Initialize
        :param message: 
        :param validation_errors: 
        :param debug: 
        '''
        self.debug = debug
        self.message = message
        self.errors = validation_errors
        if self.debug:
            print('ParserError - init'+lineno())

    def to_hash(self):
        '''
        Convert to hash
        :return: 
        '''
        hash = {}
        hash[self.message] = self.errors
        return hash

    def to_string(self):
        '''
        Convert to string
        :return: 
        '''
        if self.debug:
            print('to_string'+lineno())
        print()
        return str(self.message)+ ' : '+str(self.errors)
