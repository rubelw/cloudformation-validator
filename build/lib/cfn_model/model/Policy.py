from __future__ import absolute_import, division, print_function
import inspect
from cfn_model.model.ModelElement import ModelElement

def lineno():
    """Returns the current line number in our program."""
    return str(' - Policy - line number: '+str(inspect.currentframe().f_back.f_lineno))


class Policy(ModelElement):
    """
    Policy model
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        self.name = None
        self.policy_document = None
        self.debug = debug

        if self.debug:
            print('__init__'+lineno())

