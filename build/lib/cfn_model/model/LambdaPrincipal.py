from __future__ import absolute_import, division, print_function
from builtins import (str)
import sys

class LambdaPrincipal:
    """
    Lambda principal model
    """
    
    @staticmethod
    def wildcard(context):
        """
        If contains wildcard
        :return: 
        """
        if type(context) == type(str()):
            if '*' in context:
                return True

        if sys.version_info[0] < 3:
            if type(context) == type(unicode()):
                if '*' in context:
                    return True

        return False
