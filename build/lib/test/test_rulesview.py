import os
import sys
import unittest
from mock import patch
from collections import OrderedDict
from contextlib import contextmanager
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
    import io
from cloudformation_validator.CustomRuleLoader import CustomRuleLoader
from cloudformation_validator.additional_custom_rules.Ec2CustomTagsRule import Ec2CustomTagsRule
from cloudformation_validator.RuleRegistry import RuleRegistry
from cloudformation_validator.result_views.RulesView import RulesView as class_to_test

def pretty(value, htchar='\t', lfchar='\n', indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) == type(dict()) or type(value) == type(OrderedDict()):

        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) == type(list()):
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestRulesView(unittest.TestCase):
    """
    Test rules view
    """

    def test_emit(self):

      expected_result ="##################################\n\
########## WARNINGS ##############\n\
##################################\n\
##################################\n\
########## FAILINGS #############\n\
##################################\n\
{\"id\": \"F86\", \"type\": \"VIOLATION::FAILING_VIOLATION\", \"message\": \"EC2 instance does not have the required tags of Name, ResourceOwner, DeployedBy, Project\"}"

      rule = Ec2CustomTagsRule()

      registry = RuleRegistry(debug=False)

      registry.definition('F86', 'VIOLATION::FAILING_VIOLATION', 'EC2 instance does not have the required tags of Name, ResourceOwner, DeployedBy, Project')

      registry.add_rule(violation_def=rule)

      with captured_output() as (out, err):
          class_to_test.emit(rule_registry=registry, profile=None, debug=False)
      # This can go inside or outside the `with` block
      output = out.getvalue().strip()


      self.maxDiff = None

      print('expected results: ' + str(expected_result))
      print('real results: ' + str(output))

      self.assertEqual(expected_result, output)


