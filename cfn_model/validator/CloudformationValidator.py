from __future__ import absolute_import, division, print_function
import sys
import inspect
from pykwalify.core import Core
from cfn_model.validator import SchemaGenerator
from schema import Schema, And, Use, Optional, SchemaError

def lineno():
    """Returns the current line number in our program."""
    return str(' -  CloudformationValidator- line number: '+str(inspect.currentframe().f_back.f_lineno))

class CloudformationValidator:
    """
    Cloudformation validator
    """
    def __init__(self, debug=False):
        """
        Initialize
        :param debug:
        """

        self.debug = debug

        if self.debug:
            print('CloudformationValidator - __init__'+lineno())

    def validate(self, cloudformation_string):
        """
        Validating the schema for a cloudformation segment
        :param cloudformation_string:
        :return:
        """
        if self.debug:
            print("\n\n##################################################")
            print('CloudformationValidator - validate - validating following string'+lineno())

            print(str(cloudformation_string)+lineno())
            print("#######################################################\n\n")

        schema = SchemaGenerator.SchemaGenerator(debug=self.debug)
        main_schema = schema.generate(cloudformation_string)

        if self.debug:
            print('main_schema: '+str(main_schema)+lineno())

        ## create validator
        c = Core(source_data=cloudformation_string, schema_data=main_schema)
        c.validate(raise_exception=False)

        if len(c.errors)>0:
            if self.debug:
                print('errors: '+str(c.errors)+lineno())
            #raise ParserError.new('Basic CloudFormation syntax error', errors)

        # Return any validation error
        return c.errors

    def check(self, conf_schema, conf):
        """
        ???
        :param conf_schema:
        :param conf:
        :return:
        """

        try:
            conf_schema.validate(conf)
            return True
        except SchemaError:
            return False

        conf_schema = Schema({
            'version': And(Use(int)),
            'info': {
                'conf_one': And(Use(float)),
                'conf_two': And(Use(str)),
                'conf_three': And(Use(bool)),
                Optional('optional_conf'): And(Use(str))
            }
        })

        conf = {
            'version': 1,
            'info': {
                'conf_one': 2.5,
                'conf_two': 'foo',
                'conf_three': False,
                'optional_conf': 'bar'
            }
        }

        if self.debug:
            print(check(conf_schema, conf))

            print('validate')