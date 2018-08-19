from __future__ import absolute_import, division, print_function
import inspect
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' - SimpleStdoutResults - line number: '+str(inspect.currentframe().f_back.f_lineno))

class SimpleStdoutResults:
    """
    Simple standard out results
    """
    def __init__(self):
        """
        Initialize SimpleStdoutResults
        """
        print('SimpleStdoutResults - init'+lineno())

    def message_violations(self, violations):
        print('message_violations'+lineno())
        # FIXME
        sys.exit(1)

    def render(self, results):
        """
        Render results
        :param results:
        :return:
        """
        # FIXME
        sys.exit(1)
        return('render'+lineno())

    def message(self, message_type,  message, logical_resource_ids=None):
        """
        Does something with message
        :param message_type:
        :param message:
        :param logical_resource_ids:
        :return:
        """
        print('message'+lineno())
        # FIXME
        sys.exit(1)