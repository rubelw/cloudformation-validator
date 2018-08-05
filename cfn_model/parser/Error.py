from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)


def lineno():
    """Returns the current line number in our program."""
    return str(' -  Error- line number: '+str(inspect.currentframe().f_back.f_lineno))


class Error(Exception):
   """
   Base class for other exceptions
   """

   def __init__(self, message, debug=False):
       """
       Initialize
       :param message: 
       :param debug: 
       """
       self.debug = debug

       if self.debug:
           print('__init__ - Error'+lineno())

       try:
           ln = sys.exc_info()[-1].tb_lineno
       except AttributeError:
           ln = inspect.currentframe().f_back.f_lineno
       self.args = "{0.__name__} (line {1}): {2}".format(type(self), ln, message),
       
       # FIXME
       sys.exit(self)
