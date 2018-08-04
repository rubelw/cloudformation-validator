"""
The command line interface to cfn_nagger.

"""
from __future__ import absolute_import, division, print_function
import sys
import click
import inspect
import cloudformation_validator
from cloudformation_validator import ValidateUtility
from cloudformation_validator.RuleDumper import RuleDumper


def lineno():
    """Returns the current line number in our program."""
    return str(' - ValidateUtility - line number: '+str(inspect.currentframe().f_back.f_lineno))



@click.group()
@click.version_option(version='0.5.4')
def cli():
    pass


@cli.command()
@click.option('--suppress-errors','-s',help='Suppress warnings like bad file format, etc', required=False, is_flag=True)
@click.option('--template-path', '-t', help='base directory to search for templates', required=False)
@click.option('--template-file', '-f', help='single_template_file', required=False)
@click.option('--debug',help='Turn on debugging', required=False, is_flag=True)
@click.option('--rules-directory', '-r', help='Extra rule directory', required=False)
@click.option('--profile-path', '-o', help='Path to a profile file', required=False)
@click.option('--allow-suppression/--no-allow-suppression', help='Allow using Metadata to suppress violations', default=True, required=False)
@click.option('--print-suppression','-p', help='Emit suppressions to stderr', required=False, is_flag=True)
@click.option('--parameter-values-path', '-m', help='Path to a JSON file to pull Parameter values from', required=False)
@click.option('--isolate-custom-rule-exceptions', '-i', help='Isolate custom rule exceptions - just emit the exception without stack trace and keep chugging',is_flag=True)
@click.option('--version', '-v', help='Print version and exit', required=False, is_flag=True)
def validate(suppress_errors,template_path,template_file,debug,rules_directory,profile_path,allow_suppression,print_suppression,parameter_values_path,
             isolate_custom_rule_exceptions,version):
    '''
    primary function for validating a template
    :param template_path:
    :param template_file:
    :param debug:
    :param rules_directory:
    :param profile_path:
    :param allow_suppression:
    :param print_suppression:
    :param parameter_values_path:
    :param isolate_custom_rule_exceptions:
    :param version:
    :return:
    '''

    if debug:
        debug = True
    else:
        debug = False

    if version:
        myversion()
    else:

        if not template_path and not template_file:
            print('Must have either an input_path or template_file')
            sys.exit(1)

        start_validate(
            suppress_errors,
            template_path,
            template_file,
            debug,
            rules_directory,
            profile_path,
            allow_suppression,
            print_suppression,
            parameter_values_path,
            isolate_custom_rule_exceptions
        )


@cli.command()
@click.option('--profile-path', '-o', help='Path to a profile file', required=False)
@click.option('--rule-directory', '-r', help='Extra rule directory', required=False)
@click.option('--debug',help='Turn on debugging', required=False, is_flag=True)
def dump_rules(debug, rule_directory, profile_path):

    start_dump_rules(rule_directory=rule_directory, debug=debug, profile_definition=profile_path)

@click.option('--version', '-v', help='Print version and exit', required=False, is_flag=True)
def version(version):
    myversion()


def start_dump_rules(rule_directory, profile_definition, debug):

    dumper = RuleDumper(profile_definition=profile_definition, rule_directory=rule_directory, debug=debug)
    dumper.dump_rules()



def myversion():
    '''
    Gets the current version
    :return: current version
    '''
    print('Version: '+str(cloudformation_validator.__version__))

def start_validate(
        suppress_errors,
        template_path,
        template_file,
        debug,
        rules_directory,
        profile_path,
        allow_suppression,
        print_suppression,
        parameter_values_path,
        isolate_custom_rule_exceptions):
    '''
    Starts the validation
    :param template_path:
    :param template_file:
    :param debug:
    :param rules_directory:
    :param profile_path:
    :param allow_suppression:
    :param print_suppression:
    :param parameter_values_path:
    :param isolate_custom_rule_exceptions:
    :return:
    '''
    if debug:
        print('command - start_validate'+lineno())
        print('input_path: '+str(template_path))

    config_dict = {}
    config_dict['suppress_errors']=suppress_errors
    config_dict['input_path'] = template_path
    config_dict['template_file'] = template_file
    config_dict['debug'] = debug
    config_dict['rules_directory'] = rules_directory
    config_dict['profile'] = profile_path
    config_dict['allow_suppression'] = allow_suppression
    config_dict['print_suppression'] = print_suppression
    config_dict['parameter_values_path'] = parameter_values_path
    config_dict['isolate_custom_rule_exceptions'] = isolate_custom_rule_exceptions
    validator = ValidateUtility(config_dict)
    if debug:
        print('print have validator')
    if validator.validate():
        if debug:
            print('validated')
    else:
        if debug:
            print('not validated')