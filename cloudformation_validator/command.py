"""
The command line interface to cfn_nagger.

"""
from __future__ import absolute_import, division, print_function
import sys
import click
import inspect
import subprocess
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
@click.option('--use-optional-rules',help='Use optional rules', required=False, is_flag=True)
def validate(suppress_errors,template_path,template_file,debug,rules_directory,profile_path,allow_suppression,print_suppression,parameter_values_path,
             isolate_custom_rule_exceptions,version, use_optional_rules):
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
    :param use_optional_rules
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
            isolate_custom_rule_exceptions,
            use_optional_rules
        )


@cli.command()
@click.option('--profile-path', '-o', help='Path to a profile file', required=False)
@click.option('--rule-directory', '-r', help='Extra rule directory', required=False)
@click.option('--debug',help='Turn on debugging', required=False, is_flag=True)
def dump_rules(debug, rule_directory, profile_path):
    """
    dump rules
    :param debug:
    :param rule_directory:
    :param profile_path:
    :return:
    """
    start_dump_rules(rule_directory=rule_directory, debug=debug, profile_definition=profile_path)

@click.option('--version', '-v', help='Print version and exit', required=False, is_flag=True)
def version(version):
    """
    Get version
    :param version:
    :return:
    """
    myversion()


def start_dump_rules(rule_directory, profile_definition, debug):
    """
    start dumping rules
    :param rule_directory:
    :param profile_definition:
    :param debug:
    :return:
    """
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
        isolate_custom_rule_exceptions,
        use_optional_rules):
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
    :param use_optional_rules
    :return:
    '''
    if debug:
        print('command - start_validate'+lineno())
        print('input_path: '+str(template_path))

    check_for_updates(debug=debug)


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
    config_dict['use_optional_rules'] = use_optional_rules
    validator = ValidateUtility(config_dict)
    if debug:
        print('print have validator')
    if validator.validate():
        if debug:
            print('validated')
    else:
        if debug:
            print('not validated')


def get_current_pip_version(debug=False):

    try:
        command = 'pip search cloudformation-validator | grep cloudformation-validator | cut -d\' \' -f 2 |  sed -e "s/^(//" -e "s/)//"'
        if debug:
            print('command: '+str(command))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        if stdout:
            current_pip_version = str(stdout).rstrip('\n').strip()
            return current_pip_version
        if stderr:
            print('Error setting up build number')
            elines = stderr.splitlines()
            for e in elines:
                print((e))

    except Exception as e:
        print('Error trying to determine the current cloudformation-validator version')
        return 0

def check_for_updates(debug=False):

    try:
        current_pip_version = get_current_pip_version(debug=debug)
        current_local_version = str(cloudformation_validator.__version__).rstrip('\n').strip()
        if debug:
            print('current pypi version: '+str(current_pip_version))
            print('current local version: '+str(current_local_version))

        if current_pip_version == 0:
            raise Exception
        elif current_pip_version != current_local_version:
            print('#########################################################################################')
            print('There is a more current version of cloudformation-validator. You should update ')
            print('cloudformation-validator with pip install -U cloudformation-validator')
            print('#########################################################################################')
            sys.exit(1)
        else:
            if debug:
                print('cloudformation-validator is the most current version')
    except Exception as e:
        print('Error trying to determine the current cloudformation-validator version')
