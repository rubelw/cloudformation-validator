from __future__ import absolute_import, division, print_function
import re
import inspect
from cloudformation_validator.Profile import Profile
from cfn_model.parser.ParserError import ParserError


def lineno():
    """Returns the current line number in our program."""
    return str(' - ProfileLoader - line number: '+str(inspect.currentframe().f_back.f_lineno))



# Load rule profile
class ProfileLoader:
    """
    Profile loader
    """

    def __init__(self,rules_registry,debug=False):
        """
        Initialize the ProfileLoader
        :param rules_registry:
        :param debug:
        """
        self.debug = debug
        self.rules_registry = rules_registry

        if self.debug:
            print('ProfileLoader - init'+lineno())

    def load(self, profile_definition):
        """
        Load rules from a profile definition
        :param profile_definition:
        :return:
        """
        if self.debug:
            print('load'+lineno())
            print('vars: '+str(vars(profile_definition))+lineno())

        # coerce falsy profile_definition into empty string for
        # empty profile check

        if not profile_definition:
            raise ParserError("Empty profile")

        new_profile = Profile()

        if self.debug:
            print('vars: '+str(vars(new_profile))+lineno())

        for definition in profile_definition.rules:
            if self.debug:
                print('definition: '+str(definition))
            rule_id = self.rule_line_match(definition.id)

            if rule_id:
                self.check_valid_rule_id(rule_id)
                new_profile.add_rule(rule_id)

        return new_profile


    def rule_line_match(self, rule_id):
        """
        Parses a line, returns first matching line or false if no match
        :param rule_id:
        :return:
        """
        if self.debug:
            print('rule_line_match'+lineno())
            print('rule_id: '+str(rule_id)+lineno())

        rule_id = rule_id.rstrip('\r\n')

        matchObj = re.match(r'^([a-zA-Z]*?[0-9]+)\s*(.*)', rule_id, re.M | re.I)

        if matchObj:
            if self.debug:
                print("matchObj.group() : "+str(matchObj.group()))
                print("matchObj.group(1) : "+str(matchObj.group(1)))
                print("matchObj.group(2) : "+str(matchObj.group(2)))
            return matchObj.group(1)
        else:
            if self.debug:
                print("No match!!")
            return False


    def rules_ids(self):
        """
        Returns ids of rules in registry
        :return:
        """
        if self.debug:
            print('rules_ids'+lineno())

        ids = []

        for rules in self.rules_registry:
            ids.append(rules.id)




    def check_valid_rule_id(self, rule_id):
        """
        Returns true if rule_id is valid (present in rules registry), else raise an error
        :param rule_id:
        :return:
        """
        if self.debug:
            print('check_valid_rule_id'+lineno())
            print('rule_id: '+str(rule_id)+lineno())

        if self.rules_registry.by_id(rule_id) == None:

            return False

        return True