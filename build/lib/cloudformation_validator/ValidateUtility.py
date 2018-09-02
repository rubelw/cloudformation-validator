from __future__ import absolute_import, division, print_function
import logging
import json
import sys
import os
import traceback
import inspect
import yaml
import re
import tempfile
import shutil
from cfn_model.parser import CfnParser
from cloudformation_validator.CustomRuleLoader import CustomRuleLoader
from cloudformation_validator.ProfileLoader import ProfileLoader
from cloudformation_validator.TemplateDiscovery import TemplateDiscovery
from cloudformation_validator.Violation import Violation
from cloudformation_validator.result_views.JsonResults import JsonResults
from cloudformation_validator.result_views.SimpleStdoutResults import SimpleStdoutResults
from cfn_model.parser.ParserError import ParserError

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def lineno():
    """Returns the current line number in our program."""
    return str(' - ValidateUtility - line number: '+str(inspect.currentframe().f_back.f_lineno))

class GenericScalar:
    def __init__(self, value, tag, style=None):
        self._value = value
        self._tag = tag
        self._style = style

    @staticmethod
    def to_yaml(dumper, data):
        # data is a GenericScalar
        return dumper.represent_scalar(data._tag, data._value, style=data._style)


def default_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return GenericScalar(node.value, tag_suffix, style=node.style)
    else:
        raise NotImplementedError('Node: ' + str(type(node)))



class ValidateUtility:


    _template = None

    def __init__(self, config_block):
        """
        Initialize ValidateUtility
        :param config_block: 
        """
        self.input_path = None
        self.template_file = None
        self.debug = False
        self.profile_path = None
        self.rules_directory = None
        self.optional_rules_directory = None
        self.allow_suppression = True
        self.print_suppression = False
        self.isolate_custom_rule_exceptions = False
        self.print_suppression = True
        self.parameter_values_path = None
        self.isolate_custom_rule_exceptions = True
        self.suppress_errors = False
        self.use_optional_rules = False
        self.excluded_rules = []
        self.s3_bucket_name = None
        self.s3_profile = None




        if config_block:
            self._config = config_block
        else:
            logging.error('config block was garbage')
            raise SystemError

        for key in self._config:
            self.__dict__[key] = self._config[key]

        if self.use_optional_rules:
            self.optional_rules_directory = os.path.dirname(os.path.realpath(__file__))+'/additional_custom_rules'

        if self.s3_bucket_name:
            self.temp_dir_path = tempfile.mkdtemp()
        else:
            self.temp_dir_path = None

        if self.debug:
            print('s3 bucket: '+str(self.s3_bucket_name))
            print('temp directory: '+str(self.temp_dir_path))



        self.custom_rule_loader = CustomRuleLoader(
            isolate_custom_rule_exceptions=self.isolate_custom_rule_exceptions,
            allow_suppression=self.allow_suppression,
            print_suppression=self.print_suppression,
            debug=self.debug,
            additional_rules_directory = self.optional_rules_directory,
            excluded_rules=self.excluded_rules,
            s3_bucket_name = self.s3_bucket_name,
            temp_dir_path = self.temp_dir_path,
            s3_profile = self.s3_profile)

        # If we have an extra rules directory
        if self.rules_directory:
            self.custom_rule_loader.extra_rule_directory = self.rules_directory


        self.custom_rule_loader.rule_directory=str(os.path.dirname(os.path.realpath(__file__))+'/custom_rules')

        self.input_path = self.validate_path(self.input_path)
        self.template_file = self.validate_path(self.template_file)
        self.rules_directory = self.validate_path(self.rules_directory)
        self.profile_path = self.validate_path(self.profile_path)


    def validate(self):
        """
        Validate a directory or file
        :return: rendered results
        """

        if self.debug:
            print('ValidateUtility - validate'+lineno())

        input_path = self.input_path
        if self.debug:
            print('input_path: '+str(input_path)+lineno())


            print('\n\n############################################')
            print('audit_audit_aggregate_across_files_and_render_results')
            print('################################################\n\n')


        aggregate_results = self.audit_aggregate_across_files_and_render_results(input_path=input_path)

        if self.debug:
            print('aggregate_results '+str(aggregate_results)+lineno())

        rendered_results =  self.render_results(aggregate_results=aggregate_results, output_format='json')


        if self.debug:
            print('rendered_results: '+str(rendered_results)+lineno())

        try:
            print(rendered_results)
            return rendered_results
        except Exception as e:
            return e


    def audit_aggregate_across_files_and_render_results(self,input_path=None, parameter_values_path=None, template_pattern=None):
        """
        Aggregate across files and render results
        :param input_path: 
        :param parameter_values_path: 
        :param template_pattern: 
        :return: 
        """
        if self.debug:
            print('ValidateUtility - audit_aggregate_across_files_and_render_results'+lineno())

        aggregate_results = self.audit_aggregate_across_files(input_path=input_path)

        if self.debug:
            print('results: '+str(aggregate_results)+lineno())

        return aggregate_results

    def audit_aggregate_across_files(self,input_path=None, parameter_values_path=None, template_pattern=None):
        """
        Given a file or directory path, return aggregate results
        :param input_path: 
        :param parameter_values_path: 
        :param template_pattern: 
        :return: 
        """
        if self.debug:
            print('ValidateUtility - audit_aggregate_across_files'+lineno())
            print('input_path: '+str(input_path)+lineno())

        if parameter_values_path:
            with open(parameter_values_path,'r') as myparamsfile:
                param_data = myparamsfile.read().replace('\n','')

            parameter_values_string = param_data
        else:
            parameter_values_string = None

        if not self.template_file:
            templates_obj = TemplateDiscovery(input_json_path=input_path,debug=self.debug)
            templates = templates_obj.discover_templates()
        else:
            templates=[self.template_file]

        if self.debug:
            print(templates)

        aggregate_results = []

        for template in templates:

            if self.debug:
                print('template: '+str(template)+lineno())
                print('type: '+str(type(template))+lineno())

            if not self.suppress_errors:
                print("\nEvaluating: "+str(template))

            json_matchObj = re.match(r'.*.json$', template, re.M | re.I)
            yaml_matchObj = re.match(r'.*.ya*ml$',template, re.M | re.I)




            if json_matchObj:

                with open(template, 'r') as myfile:
                    if self.debug:
                        print("\n"+'Auditing file: '+str(template)+lineno())

                    json_acceptable_string = myfile.read().strip("'<>() ")
                    json_acceptable_string=json_acceptable_string.replace("'","\'")

                    if self.debug:
                        print(json_acceptable_string)

                    try:
                        data = json.loads(json_acceptable_string)
                    except Exception as e:

                        if not self.suppress_errors:
                            print("\n##############################")
                            print("Invalid json file - "+str(template)+' - skipping file')
                            print("################################\n")

                        data = {}
                    file_results = self.audit(cloudformation_string=data,parameter_values_string= parameter_values_string)

                    if self.debug:
                        print('file results: '+str(file_results)+lineno())

                    results = {}

                    if 'failure_count' in file_results:
                        results['failure_count'] = file_results['failure_count']
                    else:
                        results['failure_count']= 1
                    results['filename'] = template
                    results['file_results'] = file_results
                    aggregate_results.append(results)

            elif yaml_matchObj:

                yaml.add_multi_constructor('', default_constructor, Loader=yaml.SafeLoader)
                yaml.add_representer(GenericScalar, GenericScalar.to_yaml, Dumper=yaml.SafeDumper)

                with open(template, 'r') as myfile:
                    try:

                        data = myfile.read()
                        data = yaml.safe_load(data)

                    except Exception as e:
                        print("\n##############################")
                        print("Invalid yaml file - " + str(template) + ' - skipping file')
                        print("################################\n")

                    file_results = self.audit(cloudformation_string=data,
                                              parameter_values_string=parameter_values_string)

                    if self.debug:
                        print('file results: ' + str(file_results) + lineno())

                    results = {}

                    if 'failure_count' in file_results:
                        results['failure_count'] = file_results['failure_count']
                    else:
                        results['failure_count'] = 1
                    results['filename'] = template
                    results['file_results'] = file_results
                    aggregate_results.append(results)

            else:
                try:
                    json_stuff = open(template)
                    my_template = json.load(json_stuff)

                    if my_template and 'Resources' in my_template:
                        if self.debug:
                            print('file is json '+lineno())

                        with open(template, 'r') as myfile:
                            if self.debug:
                                print("\n" + 'Auditing file: ' + str(template) + lineno())

                            json_acceptable_string = myfile.read().strip("'<>() ")
                            json_acceptable_string = json_acceptable_string.replace("'", "\'")

                            if self.debug:
                                print(json_acceptable_string)

                            try:
                                data = json.loads(json_acceptable_string)
                            except Exception as e:

                                if not self.suppress_errors:
                                    print("\n#################################")
                                    print("Invalid json file - " + str(template) + ' - skipping file')
                                    print("################################\n")

                                data = {}
                            file_results = self.audit(cloudformation_string=data,
                                                      parameter_values_string=parameter_values_string)

                            if self.debug:
                                print('file results: ' + str(file_results) + lineno())

                            results = {}

                            if 'failure_count' in file_results:
                                results['failure_count'] = file_results['failure_count']
                            else:
                                results['failure_count'] = 1
                            results['filename'] = template
                            results['file_results'] = file_results
                            aggregate_results.append(results)

                    else:
                        if self.debug:
                            print('file is not json template'+lineno())
                except Exception as x:
                    if self.debug:
                        print('Exception caught in determining whether json template: '+str(x)+lineno())


        return aggregate_results

    def audit(self, cloudformation_string, parameter_values_string=None):
        """
        Audit files
        :param cloudformation_string: 
        :param parameter_values_string: 
        :return: 
        """
        if self.debug:
            print('ValidateUtility - audit'+lineno())

        violations = []

        parser = CfnParser.CfnParser(debug=self.debug)

        schema_validation_errors = None

        try:
            cfn_model = parser.parse(cloudformation_string, parameter_values_string)
        except Exception as e:
            if self.debug:
                print('exception: '+str(e)+lineno())
                print('type: '+str(type(e))+lineno())
                if hasattr(e, 'to_hash'):
                    print('to_hash: '+str(e.to_hash())+lineno())
            cfn_model = None
            tb = sys.exc_info()[-1]
            if self.debug:
                print('tb: ' + str(tb) + lineno())
            stk = traceback.extract_tb(tb, 1)
            if self.debug:
                print('stk: ' + str(stk) + lineno())
            fname = stk[0][2]

            if not self.suppress_errors:
                print('The failing function was', fname, lineno())
                print('error:'+str(e)+lineno())

            if hasattr(e, 'to_hash'):
                schema_validation_errors=e.to_hash()
            else:
                schema_validation_errors=e
        if self.debug:
            if cfn_model:
                print('cfn_model: '+str(dir(cfn_model))+lineno())
                print('cfn_model: '+str(vars(cfn_model))+lineno())
                print(dir(cfn_model))

                for parameters in cfn_model.parameters:
                    print('parameter: '+str(parameters))
                    print(cfn_model.parameters[parameters])

                print("\n\n###############################")
                print('Done parsing parameters'+lineno())
                print("###############################\n\n")

                for resource in cfn_model.resources:
                    print('resource: '+str(resource))
                    print(cfn_model.resources[resource])
                    print('vars: '+str(vars(cfn_model.resources[resource])))
                    print('dir: '+str(dir(cfn_model.resources[resource])))
                    for attr in dir(cfn_model.resources[resource]):
                        print("obj.%s = %r" % (attr, getattr(cfn_model.resources[resource], attr)))

                print("\n\n###############################")
                print('Done parsing resources'+lineno())
                print("###############################\n\n")
                print('model is loaded'+lineno())

                print('vars: '+str(vars(cfn_model))+lineno())
                print('parameters: '+str(cfn_model.parameters))

        if not schema_validation_errors:
            if cfn_model:
                # Get any violations from custom rules
                # custom rules are in addition to the normal rules
                violations = self.custom_rule_loader.execute_custom_rules(cfn_model)

            if self.debug:
                print('violations: '+str(violations)+lineno())

                print("\n\n###############################")
                print('Done loading custom rules'+lineno())
                print("###############################\n\n")

            if len(violations)<1:
                failure_count = 0
            else:

                failure_count = self.count_failures(violations)
                if self.debug:
                    print('failure count: '+str(failure_count)+lineno())

                warning_count = self.count_warnings(violations)
                if self.debug:
                    print('warning count: '+str(warning_count))

            if self.debug:
                print('count: '+str(failure_count)+lineno())

            violations = self.filter_violations_by_profile(
                {
                    'failure_count': self.count_failures(violations),
                    'violations' : violations
                }
            )

            if self.debug:
                print('violations: '+str(violations)+lineno())
            return violations
        else:
            if self.debug:
                print('there are schema validation errors '+lineno())

            violation = Violation('FATAL','VIOLATION::FAILING_VIOLATION', str(schema_validation_errors))
            violations.append(violation)

            return violations

    def filter_violations_by_profile(self, violations):
        """
        Filter the violation by profile
        :param violations: 
        :return: filtered violations
        """
        profile = None

        new_violations = []

        if self.debug:
            print('violations: '+str(violations)+lineno())

        failure_count = violations['failure_count']

        if not self.profile_path:
            if self.debug:
                print('profile definition: '+str(self.profile_path)+lineno())

            try:
                profile_loader = ProfileLoader(self.custom_rule_loader.rule_definitions(),debug=self.debug)

                profile = profile_loader.load(self.custom_rule_loader.rule_definitions())
                if self.debug:
                    print('rule ids in profile: '+str(profile.rule_ids)+lineno())

            except ParserError as e:
                print('Error'+str(e)+lineno())
                sys.exit(1)
        else:
            print('has a profile path '+lineno())
            print('Need to fix for loading a profile')
            sys.exit(1)
            #profile = self.profile_path

        if profile:
            if self.debug:
                print('violations: '+str(violations)+lineno())
                print('violations: '+str(violations['violations'])+lineno())

            for v in violations['violations']:
                if self.debug:
                    print('violation: '+str(v)+lineno())

                if self.debug:
                    print('violation: '+str(v)+lineno())
                if hasattr(v,'id'):
                    if v.id:
                        if self.debug:
                            print('id: '+str(v.id)+lineno())

                        if profile.execute_rule(v.id):
                            new_violations.append(v)
        if self.debug:
            print('new_violations: '+str(new_violations)+lineno())

        results = {'failure_count':str(failure_count), 'violations':new_violations}
        return results


    def _get_schemas(self, type):
        """
        Get the schemas
        :param type: 
        :return: 
        """
        if self.debug:
            print('ValidateUtility - _get_schemas'+lineno())

        results = os.listdir(os.getcwd()+'/cloudformation_validator/test_templates/json')

        if self.debug:
            print(results)

        if type in results:
            results = os.listdir(os.getcwd() + '/cloudformation_validator/test_templates/json/'+type)
            if self.debug:
                print(results)
            return results

    def _check_structure(self, conf_structure, my_conf):
        """
        Check structure
        :param conf_structure: 
        :param my_conf: 
        :return: 
        """
        if self.debug:
            print('ValidateUtility - check structure'+lineno())
            print('type: '+str(type(conf_structure))+lineno())
            print('type: '+str(type(my_conf))+lineno())

            for k in conf_structure:
                print(k)

        if sorted(my_conf.keys()) != sorted(conf_structure.keys()):
            if self.debug:
                print('sorted keys is not equal'+lineno())
            return False

        if self.debug:
            print('keys in proper order'+lineno())

        for key in my_conf.keys():
            if self.debug:
                print('key: '+str(key))
            if type(my_conf[key]) != type(dict()):
                return False
            else:
                if sorted(my_conf[key].keys()) != sorted(conf_structure[key].keys()):
                    return False

        return True

    def _fix_JSON(self, json_message=None):
        """
        Fix JSON
        :param json_message: 
        :return: 
        """
        
        result = None
        
        try:
            result = json.loads(json_message)
        except Exception as e:
            # Find the offending character index:
            idx_to_replace = int(str(e).split(' ')[-1].replace(')', ''))
            # Remove the offending character:
            json_message = list(json_message)
            json_message[idx_to_replace] = ' '
            new_message = ''.join(json_message)
            return self._fix_JSON(json_message=new_message)
        return result

    def render_results(self, aggregate_results, output_format):
        """
        Render results
        :param aggregate_results: 
        :param output_format: 
        :return: rendered results
        """

        if self.debug:
            print('ValidateUtility - render_results'+lineno())
            print('aggregate_results: '+str(aggregate_results)+lineno())

        renderer = self.results_renderer(output_format)
        return renderer.render(aggregate_results)


    def results_renderer(self, output_format='txt'):
        """
        Sets the format for the rendered results
        :param output_format: 
        :return: 
        """

        if self.debug:
            print('ValidateUtility - results_renderer'+lineno())

        if output_format== 'txt':
            return SimpleStdoutResults()

        elif output_format=='json':
            return JsonResults(debug=self.debug,suppress_errors=self.suppress_errors)
        else:
            if not self.suppress_errors:
                print('there is a problem'+lineno())


    def count_warnings(self, violations):
        """
        Counts the number of warnings
        :param violations: 
        :return: warning count
        """
        if self.debug:
            print('count warnings'+lineno())

        if violations:
            if self.debug:
                print('length: '+str(len(violations))+lineno())

        count =0

        for violation in violations:
            if self.debug:
                print(violation)

            if violation:
                if hasattr(violation,'type'):
                    if violation.type:
                        if violation.type == 'VIOLATION::WARNING':
                            if str(violation.id) not in self.excluded_rules:
                                count+=int(len(violation.logical_resource_ids))
        return count

    def count_failures(self, violations):
        """
        Count the number of failures
        :param violations: 
        :return: returns the number of failures
        """
        if self.debug:
            print('count failures'+lineno())

        if violations:
            if self.debug:
                print('violations: '+str(violations)+lineno())
                print('length: '+str(len(violations))+lineno())


        count =0
        for violation in violations:
            if self.debug:
                print(str(violation)+lineno())

            if violation:
                if hasattr(violation,'type'):


                    if violation.type:
                        if violation.type == 'VIOLATION::FAILING_VIOLATION':

                            if str(violation.id) not in self.excluded_rules:
                                count+=int(len(violation.logical_resource_ids))

        return count


    def validate_path(self,path):

        if path:
            matchObj = re.match(r'^\./(.*)', path, re.M | re.I)
            if matchObj:

                return str(os.getcwd() + '/' + str(matchObj.group(1)))

            matchObj = re.match(r'^[a-zA-Z1-9].*', path, re.M | re.I)
            if matchObj:
                return str(os.getcwd() + '/' + str(matchObj.group(0)))

        return path