import sys
import os
import copy
import importlib
import inspect
from cloudformation_validator.RuleRegistry import RuleRegistry



def lineno():
    """Returns the current line number in our program."""
    return str(' - CustomRuleLoader - line number: '+str(inspect.currentframe().f_back.f_lineno))


def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


class CustomRuleLoader:


    def __init__(self, debug=False, rule_directory=None, extra_rule_directory=None, allow_suppression=True, print_suppression=False, isolate_custom_rule_exceptions=False):
        '''
        Initialize CustomRuleLoader
        :param debug: 
        :param rule_directory: 
        :param allow_suppression: 
        :param print_suppression: 
        :param isolate_custom_rule_exceptions: 
        '''
        self.debug = debug
        self.rule_directory = rule_directory
        self.extra_rule_directory = extra_rule_directory
        self.allow_suppression= allow_suppression
        self.print_suppression = print_suppression
        self.isolate_custom_rule_exceptions = isolate_custom_rule_exceptions

        self.validate_extra_rule_directory = self.rule_directory

        if self.debug:
            print('CustomRuleLoader init'+lineno())

    def rule_definitions(self):
        '''
        Loads all the rule definitions from the rules directory in to the rules registry object and
        returns the rules registry object
        :return: rules registry
        '''
        if self.debug:
            print('CustomRuleLoader - rule definitions'+str(lineno()))

        rule_registry= RuleRegistry(self.debug)

        classes = self.discover_rule_classes(self.rule_directory)

        if self.debug:
            print('number of rules: '+str(len(classes))+lineno())

        # Iterate through the rules directory and get the class for each of the rules
        for rule_class in classes:
            if self.debug:
                print(str(rule_class)+lineno())

            # Skip the base rule from which all rules are derived
            if str(rule_class)== "BaseRule":
                continue

            id, type,message = self.rule_registry_from_rule_class(rule_class)

            if self.debug:
                print('id: '+str(id)+lineno())
                print('type: '+str(type)+lineno())
                print('message: '+str(message)+lineno())

            rule_registry.definition(id,type,message)

        if self.debug:
            print('rules registry rules are now: '+str(rule_registry.rules)+lineno())

        return rule_registry


    def execute_custom_rules(self, cfn_model):
        '''
        Execute any custom rules, which are in addition to the regular rules
        :param cfn_model:
        :return:
        '''
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


    def rule_registry_from_rule_class(self, rule_class):
        '''
        Gets the rule id, type and text for a specific rule
        :param rule_class: The rule name
        :return: rule_id, rule_type, rule_text
        '''
        if self.debug:
            print('CustomRuleLoader - rule_registry_from_rule_class'+str(lineno()))
            print('rule_class: '+str(rule_class)+lineno())

        my_module = importlib.import_module("cloudformation_validator.custom_rules." + str(rule_class))

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
        '''
        Filter rules
        :param cfn_model: 
        :param violations: 
        :return: violations
        '''
        if self.debug:
            print('CustomRuleLoader - filter_rule_classes'+str(lineno()))


        # Get an array of all the rule classes
        rule_classes = self.discover_rule_classes(self.rule_directory)

        # Iterate over each of the rule classes
        for rule_class in rule_classes:

            # Ignore the base rule
            if rule_class != 'BaseRule':

                if self.debug:
                    print("\n\n##########################")
                    print('Rule is not BaseRule'+lineno())
                    print('CustomRuleLoader - filter_rule_classes - rule_class '+str(rule_class)+str(lineno()))
                    print("##########################\n\n")

                # Import the rule class
                my_module = importlib.import_module("cloudformation_validator.custom_rules."+str(rule_class))


                MyClass = getattr(my_module, str(rule_class))

                if self.debug:
                    print('debug is currently: '+str(self.debug)+lineno())

                #setattr(MyClass,'debug',self.debug)

                if self.debug:
                    print("\n\n#############################################")
                    print('Created new '+str(rule_class)+' class'+lineno())
                    print('rule class: '+str(rule_class)+lineno())
                    print("################################################\n")

                # Sets the cfn_model in the rule class
                instance = MyClass(cfn_model,debug=self.debug)

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
                    #for attr in dir(instance):
                    #    print("obj.%s = %r" % (attr, getattr(instance, attr))+lineno())
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
                    violations.append((audit_result))

                #rescue Exception = > exception
                #raise exception unless @ isolate_custom_rule_exceptions
                #STDERR.puts exception

        return violations



    def rules_to_suppress(self, resource):
        '''
        Rules to suppress
        :param resource: 
        :return: 
        '''
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


    def validate_cfn_nag_metadata(self,cfn_model):
        '''
        Validate the metadata
        :param cfn_model: 
        :return: 
        '''
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
        '''
        Supress certain resources
        :param rules_to_suppress: 
        :param rule_id: 
        :param logical_resource_id: 
        :return: 
        '''
        if self.debug:
            print('CustomRuleLoader - suppress_resource'+str(lineno()))

        sys.exit(1)
        #FIXME
        found_suppression_ruile = self.rules_to_suppress()
        #found_suppression_rule = rules_to_suppress.find do |rule_to_suppress|
        #  next if rule_to_suppress['id'].nil?
        #  rule_to_suppress['id'] == rule_id
        #end
        #if found_suppression_rule && @print_suppression
        #  STDERR.puts "Suppressing #{rule_id} on #{logical_resource_id} for reason: #{found_suppression_rule['reason']}"
        #end
        #!found_suppression_rule.nil?


    def cfn_model_with_suppressed_resources_removed(self, cfn_model, rule_id, allow_suppression):
        '''
        CFN model with suppressed resources removed
        :param cfn_model: 
        :param rule_id: 
        :param allow_suppression: 
        :return: 
        '''
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
        '''
        Validate the extra rules directory
        :param rule_directory: 
        :return: 
        '''
        if self.debug:
            print('CustomRuleLoader - validate_extra_rule_directory'+str(lineno()))
            print('rule_directory: '+str(rule_directory)+lineno())

        if rule_directory == None:
            return True
        else:
            return os.path.isdir(rule_directory)


    # Get all the rules files
    def discover_rule_filenames(self):
        '''
        Discover the rule filenames
        :return: 
        '''
        if self.debug:
            print('CustomRuleLoader - discover_rule_filename'+str(lineno()))

        rule_filenames = []

        temp_rule_filenames = os.listdir(self.rule_directory)
        if self.debug:
            print('rules directory: '+str(self.rule_directory)+lineno())

        for temp_file in temp_rule_filenames:
            if not temp_file.startswith('__'):
            #if temp_file != '__init__.py' and temp_file != '__pycache__':

                if temp_file.endswith('.py'):
                    rule_filenames.append(str(temp_file).replace('.py',''))
                #elif temp_file.endswith('.pyc'):
                #    rule_filenames.append(str(temp_file).replace('.pyc',''))


        if self.extra_rule_directory:
            temp_rule_filenames = os.listdir(self.extra_rule_directory)
            if self.debug:
                print('rules directory: ' + str(self.extra_rule_directory) + lineno())

            for temp_file in temp_rule_filenames:
                if not temp_file.startswith('__'):
                #if temp_file != '__init__.py' and temp_file != '__pycache__':
                    #if temp_file.endswith('.pyc'):

                    #    new_filename = temp_file.replace('.pyc','')

                    #    if self.debug:
                    #        print('new filename: '+str(new_filename)+lineno())

                    #    rule_filenames.append(str(new_filename))
                    if temp_file.endswith('.py'):

                        new_filename = temp_file.replace('.py','')

                        if self.debug:
                            print('new filename: '+str(new_filename)+lineno())

                        rule_filenames.append(str(temp_file).replace('.py', ''))

        if self.debug:
            print('rule filenames: '+str(rule_filenames)+lineno())

        return rule_filenames


    # Get a listing of all the rule file names and import all the rule classes
    def discover_rule_classes(self, rule_directory):
        '''
        Discover the rule classes
        :param rule_directory: 
        :return: 
        '''
        if self.debug:
            print('CustomRuleLoader - discover_rule_classes'+str(lineno()))

        rule_classes = []

        rule_filenames = self.discover_rule_filenames()

        for file in rule_filenames:

            if self.debug:
                print('file: '+str(file)+lineno())

            exec("from cloudformation_validator.custom_rules import "+str(file))

        if self.debug:
            print('rule filenames: '+str(rule_filenames)+lineno())
        return rule_filenames



