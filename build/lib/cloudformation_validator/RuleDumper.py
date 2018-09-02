from __future__ import absolute_import, division, print_function
import inspect
import sys
import os
from cloudformation_validator.CustomRuleLoader import CustomRuleLoader
from cloudformation_validator.ProfileLoader import ProfileLoader
from cfn_model.parser.ParserError import ParserError
from cloudformation_validator.result_views.RulesView import RulesView


def lineno():
    """Returns the current line number in our program."""
    return str(' - RuleDumper - line number: '+str(inspect.currentframe().f_back.f_lineno))


class RuleDumper:
    """
    Rule Dumper
    """

    def __init__(self, profile_definition=None, rule_directory=None, debug=False):
        """
        Initialize RuleDumper
        :param profile_definition: 
        :param rule_directory: 
        """
        self.debug = debug
        self.rule_directory = rule_directory
        self.profile_definition = profile_definition

        if self.debug:
            print('RuleDumper - init'+lineno())

    def dump_rules(self):
        """
        Dump rules
        :return: 
        """

        custom_rule_loader = CustomRuleLoader(debug=self.debug)

        if self.rule_directory:
            custom_rule_loader.extra_rule_directory = self.rule_directory

        custom_rule_loader.rule_directory = str(os.path.dirname(os.path.realpath(__file__)) + '/custom_rules')

        rule_registry = custom_rule_loader.rule_definitions()

        profile = None

        if self.profile_definition:

            if self.debug:
                print('profile definition: '+str(self.profile_definition)+lineno())

            try:
                profile_loader = ProfileLoader(custom_rule_loader.rule_definitions(),debug=self.debug)

                profile = profile_loader.load(custom_rule_loader.rule_definitions())
                if self.debug:
                    print('rule ids in profile: '+str(profile.rule_ids)+lineno())

            except ParserError as e:
                print('Error'+str(e)+lineno())
                sys.exit(1)

        view = RulesView()
        rules_view = view.emit(rule_registry=rule_registry, profile=profile, debug=self.debug)

        if self.debug:
            print('rules_view: '+str(rules_view))
