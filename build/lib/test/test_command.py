import os
import sys
import unittest
from contextlib import contextmanager
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
    import io

from mock import patch
from collections import OrderedDict
import cloudformation_validator
from cloudformation_validator import command as class_to_test


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


class TestCommand(unittest.TestCase):
    """
    Test command class
    """

    @patch('sys.exit')
    @patch('cloudformation_validator.command.get_current_pip_version')
    def test_check_for_updates_outdated_version(self,version,exit):
        """
        Tests for when pypi version does not match current version
        :param version:
        :param exit:
        :return:
        """
        version.return_value='0.2.34'
        exit.return_value=None
        expected_results = "#########################################################################################\n" \
                  "There is a more current version of cloudformation-validator. You should update \n" \
                  "cloudformation-validator with pip install -U cloudformation-validator\n" \
                  "#########################################################################################"

        with captured_output() as (out, err):
            class_to_test.check_for_updates()
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()

        real_result = class_to_test.check_for_updates()

        self.maxDiff = None
        self.assertEqual(exit.return_value, real_result)

        self.assertEqual(output,expected_results)




    @patch('cloudformation_validator.command.get_current_pip_version')
    def test_check_for_updates_current_version(self,version):
        """
        Test for when pypi version matches current version
        :param version:
        :return:
        """
        version.return_value=cloudformation_validator.__version__

        with captured_output() as (out, err):
            class_to_test.check_for_updates()
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()

        real_result = class_to_test.check_for_updates()

        self.maxDiff = None
        self.assertEqual(output,'')


    @patch('sys.exit')
    @patch('cloudformation_validator.command.get_current_pip_version')
    def test_check_for_updates_error(self,version,exit):
        """
        Testing for when there is an error retrieving info from pypi
        :param version:
        :param exit:
        :return:
        """
        version.return_value=0
        exit.return_value=None
        expected_results = "Error trying to determine the current cloudformation-validator version"

        with captured_output() as (out, err):
            class_to_test.check_for_updates()
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()


        real_result = class_to_test.check_for_updates()

        self.maxDiff = None
        self.assertEqual(exit.return_value, real_result)

        self.assertEqual(output,expected_results)

