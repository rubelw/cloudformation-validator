from __future__ import absolute_import, division, print_function
import sys
import os
import copy
import importlib
import inspect
import boto3
from botocore.exceptions import ClientError
from cloudformation_validator.RuleRegistry import RuleRegistry

def lineno():
    """Returns the current line number in our program."""
    return str(' - CustomRuleLoader - line number: '+str(inspect.currentframe().f_back.f_lineno))

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

class CustomRuleLoader:
    """
    Custom rule loader
    """
    def __init__(self, debug=False,
                 rule_directory=None,
                 extra_rule_directory=None,
                 allow_suppression=True,
                 print_suppression=False,
                 isolate_custom_rule_exceptions=False,
                 additional_rules_directory=None,
                 excluded_rules=[],
                 s3_bucket_name=None,
                 s3_profile = None,
                 temp_dir_path=None):
        """
        Initialize CustomRuleLoader
        :param debug: 
        :param rule_directory: 
        :param allow_suppression: 
        :param print_suppression: 
        :param isolate_custom_rule_exceptions: 
        """
        self.debug = debug
        self.rule_directory = rule_directory
        self.extra_rule_directory = extra_rule_directory
        self.additional_rules_directory = additional_rules_directory
        self.allow_suppression= allow_suppression
        self.print_suppression = print_suppression
        self.isolate_custom_rule_exceptions = isolate_custom_rule_exceptions
        self.validate_extra_rule_directory = self.rule_directory
        self.excluded_rules = excluded_rules
        self.s3_bucket_name = s3_bucket_name
        self.temp_dir_path= temp_dir_path
        self.s3_profile = s3_profile

        if self.debug:
            print('CustomRuleLoader init'+lineno())

    def rule_definitions(self):
        """
        Loads all the rule definitions from the rules directory in to the rules registry object and
        returns the rules registry object
        :return: rules registry
        """
        if self.debug:
            print('CustomRuleLoader - rule definitions'+str(lineno()))

        rule_registry= RuleRegistry(self.debug)


        classes = self.discover_rule_classes(self.rule_directory)

        if self.debug:
            print('number of rule types: '+str(len(classes))+lineno())

        # Iterate through the rules directory and get the class for each of the rules
        for rule_class in classes:
            if self.debug:
                print(str(rule_class)+lineno())

            for file in classes[rule_class]:

                # Skip the base rule from which all rules are derived
                if str(file)== "BaseRule":
                    continue

                id, type,message = self.rule_registry_from_rule_class(file, classes[rule_class][file])

                if self.debug:
                    print('id: '+str(id)+lineno())
                    print('type: '+str(type)+lineno())
                    print('message: '+str(message)+lineno())

                if str(id) not in self.excluded_rules:
                    rule_registry.definition(id, type, message)

        if self.debug:
            print('rules registry rules are now: '+str(rule_registry.rules)+lineno())

        return rule_registry

    def execute_custom_rules(self, cfn_model):
        """
        Execute any custom rules, which are in addition to the regular rules
        :param cfn_model:
        :return:
        """
        if self.debug:
            print('CustomRuleLoader - execute_custom_rules'+str(lineno()))
            print('cfn_model: '+str(cfn_model)+str(lineno()))

        violations = []

        # Validate the cfn model again the metadata nagger
        cfn_model  = self.validate_cfn_nag_metadata(cfn_model)

        if self.debug:
            print('##### Done checking metadata #########'+str(lineno()))
            print('### filtering rule classes'+str(lineno()))

        violations = self.filter_rule_classes(cfn_model, violations)

        if self.debug:
            print('violations from extra rules: '+str(violations)+lineno())

        return violations

    def rule_registry_from_rule_class(self, rule_class, directory):
        """
        Gets the rule id, type and text for a specific rule
        :param rule_class: The rule name
        :return: rule_id, rule_type, rule_text
        """
        if self.debug:
            print('CustomRuleLoader - rule_registry_from_rule_class'+str(lineno()))
            print('rule_class: '+str(rule_class)+lineno())
            print('rule directory: '+str(directory))

        if 'site-packages' in str(directory) and 'additional' in str(directory):
            my_module = importlib.import_module("cloudformation_validator.additional_custom_rules." + str(rule_class))
        elif 'site-packages' in str(directory) and 'custom_rules' in str(directory):
            my_module = importlib.import_module("cloudformation_validator.custom_rules." + str(rule_class))
        elif 'cloudformation_validator' in str(directory) and 'additional' in str(directory):
            my_module = importlib.import_module("cloudformation_validator.additional_custom_rules." + str(rule_class))
        elif 'cloudformation_validator' in str(directory) and 'custom_rules' in str(directory):
            my_module = importlib.import_module("cloudformation_validator.custom_rules." + str(rule_class))
        else:
            my_module = importlib.import_module(str(rule_class))

        MyClass = getattr(my_module, str(rule_class))

        if self.debug:
            print('Created new class:'+str(rule_class) + lineno())
            print('type: '+str(type(MyClass))+lineno())
            print('vars: '+str(vars(MyClass))+lineno())

        rule = MyClass()

        if self.debug:
            print('rule: '+str(rule)+lineno())
            print('type: '+str(type(rule))+lineno())
            print('vars: '+str(vars(rule))+lineno())
            print(str(rule.rule_id()) + lineno())

        return rule.rule_id(), rule.rule_type(), rule.rule_text()

    def filter_rule_classes(self, cfn_model, violations):
        """
        Filter rules
        :param cfn_model: 
        :param violations: 
        :return: violations
        """
        if self.debug:
            print('CustomRuleLoader - filter_rule_classes'+str(lineno()))

        # Get an array of all the rule classes
        rule_classes = self.discover_rule_classes(self.rule_directory)


        # Iterate over each of the rule classes
        for rule_class in rule_classes:

            for file in rule_classes[rule_class]:

                if self.debug:
                    print('file: '+str(file)+lineno())

                # Ignore the base rule
                if file == 'BaseRule':
                    continue

                if rule_class == 'rules_directory':

                    if self.debug:
                        print("\n\n##########################")
                        print('Rule is not BaseRule'+lineno())
                        print('CustomRuleLoader - filter_rule_classes - rule_class '+str(file)+str(lineno()))
                        print("##########################\n\n")

                    # Import the rule class
                    if 'additional' in rule_classes[rule_class][file]:
                        my_module = importlib.import_module("cloudformation_validator.additional_custom_rules." + str(file))
                    else:
                        my_module = importlib.import_module("cloudformation_validator.custom_rules."+str(file))

                elif rule_class == 'extra_rules_directory':

                    if self.debug:
                        print("\n\n##########################")
                        print('Rule is not BaseRule' + lineno())
                        print('CustomRuleLoader - filter_rule_classes - rule_class ' + str(file) + str(lineno()))
                        print("##########################\n\n")

                    # Import the rule class
                    my_module = importlib.import_module(str(file))

                MyClass = getattr(my_module, str(file))

                if self.debug:
                    print('debug is currently: '+str(self.debug)+lineno())


                if self.debug:
                    print("\n\n#############################################")
                    print('Created new '+str(file)+' class'+lineno())
                    print('rule class: '+str(file)+lineno())
                    print('my class: '+str(type(MyClass))+lineno())
                    print("################################################\n")

                # Sets the cfn_model in the rule class
                instance = MyClass(cfn_model, debug=self.debug)

                if self.debug:
                    print(str(instance.rule_id())+lineno())
                    print(dir(instance))

                    print("\n\n############################")
                    print('filtering the cfn_model to remove suppressed resources'+lineno())
                    print("#################################\n\n")

                # This does nothing if cloudformation_validator allow_suppression flag is False
                filtered_cfn_model = self.cfn_model_with_suppressed_resources_removed(
                    cfn_model=cfn_model,
                    rule_id=instance.rule_id(),
                    allow_suppression=self.allow_suppression
                )

                # Set the new cfn_model to the filtered cfn_model
                instance.cfn_model = copy.copy(filtered_cfn_model)

                if self.debug:
                    print("\n\n#####################################################")
                    print('Auditing rule id: '+str(instance.rule_id())+lineno())
                    print('rule text: '+str(instance.rule_text())+lineno())
                    print('calling instance.audit '+lineno())
                    print("########################################################\n")

                # The rule is a subclass of the BaseRule.  This calls the BaseRule audit function
                audit_result = instance.audit()

                if self.debug:
                    print('audit results: '+str(audit_result)+lineno())

                # Prints audit results to stdout
                if audit_result:
                    if self.debug:
                        print(str(dir(audit_result)) + lineno())
                        print(str(vars(audit_result))+lineno())
                        print(str(audit_result.message)+lineno())

                    # Adds audit results to violation
                    violations.append(audit_result)

        return violations

    def rules_to_suppress(self, resource):
        """
        Rules to suppress
        :param resource: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - rules_to_suppress'+str(lineno()))
            print('resource: '+str(resource)+lineno())
            print('vars: '+str(vars(resource))+lineno())

        if hasattr(resource, 'metadata'):
            if resource.metadata:
                if 'cfn_nag' in resource.metadata:
                    if 'rules_to_suppres' in resource.metadata['cfn_nag']:
                        return resource.metadata['cfn_nag']['rules_to_suppress']
        else:
            if self.debug:
                print('no rules to suppress'+str(lineno()))

            return None


    def validate_cfn_nag_metadata(self, cfn_model):
        """
        Validate the metadata
        :param cfn_model: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - validate_cfn_nag_metadata'+str(lineno()))
            print('cfn_model: '+str(cfn_model)+lineno())

        mangled_metadatas = []

        for resource in cfn_model.resources:
            if self.debug:
                print('resource: '+str(resource)+lineno())
            resource_id = resource
            resource_rules_to_suppress = self.rules_to_suppress(cfn_model.resources[resource])

            if resource_rules_to_suppress:
                for rules in resource_rules_to_suppress:
                    if self.debug:
                        print('rule:'+str(rules)+lineno())

        return cfn_model


    def suppress_resource(self, rules_to_suppress, rule_id, logical_resource_id):
        """
        Supress certain resources
        :param rules_to_suppress: 
        :param rule_id: 
        :param logical_resource_id: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - suppress_resource'+str(lineno()))

        sys.exit(1)
        #FIXME
        found_suppression_ruile = self.rules_to_suppress()
        # found_suppression_rule = rules_to_suppress.find do |rule_to_suppress|
        #   next if rule_to_suppress['id'].nil?
        #   rule_to_suppress['id'] == rule_id
        # end
        # if found_suppression_rule && @print_suppression
        #   STDERR.puts "Suppressing #{rule_id} on #{logical_resource_id} for reason: #{found_suppression_rule['reason']}"
        # end
        # !found_suppression_rule.nil?


    def cfn_model_with_suppressed_resources_removed(self, cfn_model, rule_id, allow_suppression):
        """
        CFN model with suppressed resources removed
        :param cfn_model: 
        :param rule_id: 
        :param allow_suppression: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - cfn_model_with_suppressed_resources_removed'+str(lineno()))


        # Whether cloudformation_validator allow suppression is False
        if not allow_suppression:
            if self.debug:
                print('not allow suppression '+lineno())

            return cfn_model

        # If we are allowing suppression of certain rules
        else:
            if self.debug:
                print('allow suppression '+lineno())
                print('suppression is: '+str(allow_suppression))
            cfn_model = copy.copy(cfn_model)
            for resource in cfn_model.resources:
                if self.debug:
                    print(str(resource)+lineno())

                rules_to_suppress = self.rules_to_suppress(cfn_model.resources[resource])

                # Return the model if there are no rules to suppress
                if rules_to_suppress == None:
                    if self.debug:
                        print('no rules to suppress '+lineno())
                    return cfn_model
                else:
                    if self.debug:
                        print('there are rules to suppress'+lineno())
                    self.suppress_resource(rules_to_suppress,rule_id,resource)

            return cfn_model

    def validate_extra_rule_directory(self, rule_directory):
        """
        Validate the extra rules directory
        :param rule_directory: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - validate_extra_rule_directory'+str(lineno()))
            print('rule_directory: '+str(rule_directory)+lineno())

        if rule_directory == None:
            return True
        else:
            return os.path.isdir(rule_directory)

    def download_dir(self, client, resource, dist, local='/tmp', bucket='your_bucket'):
        paginator = client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    download_dir(client, resource, subdir.get('Prefix'), local, bucket)
            if result.get('Contents') is not None:
                for file in result.get('Contents'):
                    if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
                        os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
                    resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))



    def discover_rule_filenames(self):
        """
        Discover the rule filenames
        :return: A dictionary with the rules
        """
        if self.debug:
            print('CustomRuleLoader - discover_rule_filename'+str(lineno()))

        rule_filenames = {
            'rules_directory':{},
            'extra_rules_directory':{}
        }

        temp_rule_filenames = os.listdir(self.rule_directory)
        if self.debug:
            print('rules directory: '+str(self.rule_directory)+lineno())

        for temp_file in temp_rule_filenames:

            if self.debug:
                print('temp file: '+str(temp_file)+lineno())

            if not temp_file.startswith('__'):
                if temp_file.endswith('.py'):
                    rule_filenames['rules_directory'][str(temp_file).replace('.py','')] = str(self.rule_directory)

        if self.additional_rules_directory:
            temp_rule_filenames = os.listdir(self.additional_rules_directory)
            if self.debug:
                print('additional rules directory: ' + str(self.additional_rules_directory) + lineno())

            for temp_file in temp_rule_filenames:

                if self.debug:
                    print('temp file: ' + str(temp_file) + lineno())

                if not temp_file.startswith('__'):
                    if temp_file.endswith('.py'):
                        rule_filenames['rules_directory'][str(temp_file).replace('.py', '')] = str(self.additional_rules_directory)

        if self.extra_rule_directory:
            if self.debug:
                print('there is an extra rule directory '+lineno())

            temp_rule_filenames = os.listdir(self.extra_rule_directory)
            if self.debug:
                print('rules directory: ' + str(self.extra_rule_directory) + lineno())

            for temp_file in temp_rule_filenames:
                if not temp_file.startswith('__'):

                    if temp_file.endswith('.py'):

                        new_filename = temp_file.replace('.py','')

                        if self.debug:
                            print('new filename: '+str(new_filename)+lineno())

                        rule_filenames['extra_rules_directory'][str(temp_file).replace('.py', '')] = str(self.extra_rule_directory)

        if self.s3_bucket_name:

            try:

                if self.s3_profile:
                    if self.debug:
                        print('trying to create boto3 session to: '+str(self.s3_profile))
                    session = boto3.Session(profile_name=str(self.s3_profile))

                    # Any clients created from this session will use credentials
                    # from the [dev] section of ~/.aws/credentials.
                    s3 = session.resource('s3')

                else:
                    s3 = boto3.resource('s3')

                # select bucket
                my_bucket = s3.Bucket(self.s3_bucket_name)

                if self.debug:
                    print('bucket: '+str(self.s3_bucket_name))
                    print('tmp directory: '+str(self.temp_dir_path))

                # download file into current directory
                for object in my_bucket.objects.all():
                    my_bucket.download_file(object.key, os.path.join(self.temp_dir_path, object.key))

            except ClientError as e:
                print('Error getting custom rules from S3 bucket.  Check your profile and bucket name')
                print(str(e))
                sys.exit(1)

            # Get all the files downloaded from S3 to the temp directory
            temp_rule_filenames = os.listdir(self.temp_dir_path)

            if self.debug:
                print('rules directory: ' + str(self.temp_dir_path) + lineno())

            for temp_file in temp_rule_filenames:
                if not temp_file.startswith('__'):

                    if temp_file.endswith('.py'):

                        new_filename = temp_file.replace('.py', '')

                        if self.debug:
                            print('new filename: ' + str(new_filename) + lineno())

                        rule_filenames['extra_rules_directory'][str(temp_file).replace('.py', '')] = str(
                            self.temp_dir_path)


        if self.debug:
            print('rule filenames: '+str(rule_filenames)+lineno())

        return rule_filenames

    def discover_rule_classes(self, rule_directory):
        """
        Discover the rule classes
        :param rule_directory: 
        :return: 
        """
        if self.debug:
            print('CustomRuleLoader - discover_rule_classes'+str(lineno()))
            print('rule_directory: '+str(rule_directory))

        rule_classes = []

        rule_filenames = self.discover_rule_filenames()

        for directories in rule_filenames:

            if self.debug:
                print('directories: '+str(directories)+lineno())

            if directories == 'rules_directory':
                for file in rule_filenames['rules_directory']:

                    if self.debug:
                        print('file: '+str(file)+lineno())
                        print('directory: '+str(rule_filenames[directories][file]))

                    if 'additional' in str(rule_filenames[directories][file]):
                        exec("from cloudformation_validator.additional_custom_rules import "+str(file))
                    else:
                        exec("from cloudformation_validator.custom_rules import "+str(file))

            if directories == 'extra_rules_directory':
                import sys

                for file in rule_filenames['extra_rules_directory']:

                    sys.path.insert(0, rule_filenames['extra_rules_directory'][file])
                    exec("import "+str(file))

        if self.debug:
            print('rule filenames: '+str(rule_filenames)+lineno())

        return rule_filenames
