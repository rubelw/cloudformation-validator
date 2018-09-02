from __future__ import absolute_import, division, print_function
import inspect



def lineno():
    """Returns the current line number in our program."""
    return str(' - Profile - line number: '+str(inspect.currentframe().f_back.f_lineno))

class Profile:
    """
    Profile
    """
    rules_registry = None

    def __init__(self, debug=False):
        """
        Initialize profile
        :param debug:
        """
        self.debug = debug
        self.rule_ids = []

        if self.debug:
            print('Profile - init'+lineno())


    # Add a Rule to a profile
    def add_rule(self, rule_id):
        """
        Add rule to profile
        :param rule_id:
        :return:
        """
        self.rule_ids.append(rule_id)

    def execute_rule(self, rule_id):
        """
        Whether to execute the rule id
        :param rule_id:
        :return: boolean
        """
        if self.debug:
            print('rule_id: '+str(rule_id)+lineno())
            print('rule id list in profile: '+str(self.rule_ids)+lineno())
        if rule_id in self.rule_ids:
            if self.debug:
                print('found rule id in profile rules id array'+lineno())

            return True
        return False
