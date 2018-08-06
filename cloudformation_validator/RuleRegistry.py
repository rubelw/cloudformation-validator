from __future__ import absolute_import, division, print_function
import sys
import inspect
from builtins import (str)
from cloudformation_validator.RuleDefinition import RuleDefinition


def lineno():
    """Returns the current line number in our program."""
    return str(' - RuleRegistry - line number: '+str(inspect.currentframe().f_back.f_lineno))

class RuleRegistry:
    """
    Rule registry
    """
    def __init__(self, debug=False):
        """
        Initialize RulesRegistry
        :param debug: 
        """
        self.debug = debug
        self.rules = []

        if self.debug:
            print('RuleRegistry init'+lineno())


    def definition(self, id, type, message):
        """
        Add a rule definition to the registry
        :param id: 
        :param type: 
        :param message: 
        :return: 
        """
        if self.debug:
            print('definition '+lineno())

        rule_definition = RuleDefinition(id, type, message, debug=self.debug)

        if self.debug:
            print('rule_definition: '+str(rule_definition)+lineno())
            print('rule_definition id: '+str(rule_definition.id)+lineno())

        existing_def = self.by_id(rule_definition.id)

        if self.debug:
            print('existing definition: '+str(existing_def)+lineno())

        if not existing_def:
            if self.debug:
                print('adding rule '+lineno())
            self.add_rule(rule_definition)
        else:
            return existing_def



    def by_id(self, id):
        """
        Find rule definition by id
        :param id:
        :return:
        """
        if self.debug:
            print('by_id'+lineno())

        found_it = False
        if len(self.rules)>0:

            for rule in self.rules:
                if self.debug:
                  print('rule: '+str(rule))
                  print('rule id: '+str(rule.id)+lineno())


                if rule.id == str(id):
                  found_it=True
                  break

        if self.debug:
            print('found it: '+str(found_it)+lineno())

        return found_it

    def warnings(self):
        """
        Get rule warnings
        :param self:
        :return:
        """

        rules = []

        if self.debug:
            print('warnings'+lineno())

        for rule in self.rules:
            if self.debug:
                print(str(rule)+lineno())
                print('rule type: '+str(rule.type)+lineno())

            if rule.type == 'VIOLATION::WARNING':
                rules.append(rule)
        return rules

    def failings(self):
        """
        Get failing rules
        :param self:
        :return:
        """
        rules = []

        if self.debug:
            print('failings'+lineno())

        for rule in self.rules:
            if self.debug:
                print(str(rule)+lineno())
                print('rule type: '+str(vars(rule))+lineno())

            if rule.type == 'VIOLATION::FAILING_VIOLATION':
                rules.append(rule)
        return rules

    def add_rule(self, violation_def):
        """
        Add rule definition
        :param self:
        :param violation_def:
        :return:
        """
        if self.debug:
            print('add_rule'+lineno())
            print('violation_def: '+str(violation_def)+lineno())

        self.rules.append(violation_def)

        if self.debug:
            print('registry rules are now: '+str(self.rules)+lineno())
