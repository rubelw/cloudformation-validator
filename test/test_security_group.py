import os
import sys
import unittest
from collections import OrderedDict
from cloudformation_validator.ValidateUtility import ValidateUtility as class_to_test

def pretty(value, htchar='\t', lfchar='\n', indent=0):
    """
    Prints pretty json
    :param value:
    :param htchar:
    :param lfchar:
    :param indent:
    :return: pretty json
    """


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

        if items:
            items = sorted(items)
        [str(item) for item in items]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)

    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)

    else:
        return repr(str(value))

class TestSecurityGroup(unittest.TestCase):
    """
    Test security group
    """

    def test_dangling_egress_rule(self):
        expected_result = [
            {
                'failure_count': '1',
                'filename': '/json/security_group/dangling_egress_rule.json',
                'file_results': [
                    {
                        'id': 'FATAL',
                        'type': 'VIOLATION::FAILING_VIOLATION',
                        'message': '{"Unresolved logical resource ids: [\'test\']": None}',
                        'logical_resource_ids': 'None'
                    }
                ]
            }
        ]

        if sys.version_info[0] < 3:

            expected_result = [
                {
                    'failure_count': '1',
                    'filename': '/json/security_group/dangling_egress_rule.json',
                    'file_results': [
                        {
                            'id': 'FATAL',
                            'type': 'VIOLATION::FAILING_VIOLATION',
                            'message': '{"Unresolved logical resource ids: [u\'test\']": None}',
                            'logical_resource_ids': 'None'
                        }
                    ]
                }
            ]

            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]

        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + '/cloudformation_validator/test_templates/json/security_group/dangling_egress_rule.json'
        debug = True

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)



    def test_security_group_missing_properties(self):

        expected_result = [
            {
                'failure_count': '1',
                'filename': '/json/security_group/sg_missing_properties.json',
                'file_results': [
                    {
                        'id': 'FATAL',
                        'type': 'VIOLATION::FAILING_VIOLATION',
                        'message': "{'Basic CloudFormation syntax error': [Cannot find required key 'Properties'. Path: '/Resources/sg']}",
                        'logical_resource_ids': 'None'
                    }
                ]
            }
        ]

        if sys.version_info[0] < 3:
            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + '/cloudformation_validator/test_templates/json/security_group/sg_missing_properties.json'
        debug = True

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)


    def test_security_group_when_egress_is_empty(self):
        expected_result = [
            {
                'failure_count': '1',
                'filename': '/json/security_group/single_security_group_empty_ingress.json',
                'file_results': [
                    {
                        'id': 'F1000',
                        'type': 'VIOLATION::FAILING_VIOLATION',
                        'message': 'Missing egress rule means all traffic is allowed outbound.  Make this explicit if it is desired configuration',
                        'logical_resource_ids': "['sg']"
                    }
                ]
            }
        ]

        if sys.version_info[0] < 3:
            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(os.path.realpath(
            __file__))) + '/cloudformation_validator/test_templates/json/security_group/single_security_group_empty_ingress.json'
        debug = False

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)

    def test_security_group_when_inline_sg_is_open_to_world(self):
        expected_result = [
            {
                'failure_count': '2',
                'filename': '/json/security_group/two_security_group_two_cidr_ingress.json',
                'file_results': [
                    {
                        'id': 'F1000',
                        'type': 'VIOLATION::FAILING_VIOLATION',
                        'message': 'Missing egress rule means all traffic is allowed outbound.  Make this explicit if it is desired configuration',
                        'logical_resource_ids': "['sg', 'sg2']"
                    },
                    {
                        'id': 'W2',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found with cidr open to world on ingress.  This should never be true on instance.  Permissible on ELB',
                        'logical_resource_ids': "['sg2']"
                    },
                    {
                        'id': 'W27',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found ingress with port range instead of just a single port',
                        'logical_resource_ids': "['sg', 'sg2', 'sg2']"
                    },
                    {
                        'id': 'W9',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found with ingress cidr that is not /32',
                        'logical_resource_ids': "['sg2']"
                    }
                ]
            }
        ]
        if sys.version_info[0] < 3:

            expected_result = [
                {
                    'failure_count': '2',
                    'filename': '/json/security_group/two_security_group_two_cidr_ingress.json',
                    'file_results': [
                        {
                            'id': 'F1000',
                            'type': 'VIOLATION::FAILING_VIOLATION',
                            'message': 'Missing egress rule means all traffic is allowed outbound.  Make this explicit if it is desired configuration',
                            'logical_resource_ids': "['sg', 'sg2']"
                        },
                        {
                            'id': 'W2',
                            'type': 'VIOLATION::WARNING',
                            'message': 'Security Groups found with cidr open to world on ingress.  This should never be true on instance.  Permissible on ELB',
                            'logical_resource_ids': "['sg2']"
                        },
                        {
                            'id': 'W27',
                            'type': 'VIOLATION::WARNING',
                            'message': 'Security Groups found ingress with port range instead of just a single port',
                            'logical_resource_ids': "['sg', 'sg2', 'sg2']"
                        },
                        {
                            'id': 'W9',
                            'type': 'VIOLATION::WARNING',
                            'message': 'Security Groups found with ingress cidr that is not /32',
                            'logical_resource_ids': "['sg2']"
                        }
                    ]
                }
            ]

            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(os.path.realpath(
            __file__))) + '/cloudformation_validator/test_templates/json/security_group/two_security_group_two_cidr_ingress.json'
        debug = False

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)

    def test_security_group_when_has_multiple_inline_egress_rules(self):
        expected_result = [
            {
                'failure_count': '0',
                'filename': '/json/security_group/multiple_inline_egress.json',
                'file_results': [
                ]
            }
        ]

        if sys.version_info[0] < 3:
            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + '/cloudformation_validator/test_templates/json/security_group/multiple_inline_egress.json'
        debug = False

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)

    def test_two_security_groups_ingress_standalone_with_non32_cidr(self):
        expected_result = [
            {
                'failure_count': '0',
                'filename': '/json/security_group/non_32_cidr_standalone_ingress.json',
                'file_results': [
                    {
                        'id': 'W9',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found with ingress cidr that is not /32',
                        'logical_resource_ids': "['securityGroupIngress2', 'securityGroupIngress3', 'securityGroupIngress4', 'securityGroupIngress5']"
                    }
                ]
            }
        ]

        if sys.version_info[0] < 3:

            expected_result = [
                {
                    'failure_count': '0',
                    'filename': '/json/security_group/non_32_cidr_standalone_ingress.json',
                    'file_results': [
                        {
                            'id': 'W9',
                            'type': 'VIOLATION::WARNING',
                            'message': 'Security Groups found with ingress cidr that is not /32',
                            'logical_resource_ids': "['securityGroupIngress2', 'securityGroupIngress3', 'securityGroupIngress4', 'securityGroupIngress5']"
                        }
                    ]
                }
            ]


            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(os.path.realpath(
            __file__))) + '/cloudformation_validator/test_templates/json/security_group/non_32_cidr_standalone_ingress.json'
        debug = False

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)

    def test_two_security_groups_with_non32_cidr(self):
        expected_result = [
            {
                'failure_count': '0',
                'filename': '/json/security_group/non_32_cidr.json',
                'file_results': [
                    {
                        'id': 'W9',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found with ingress cidr that is not /32',
                        'logical_resource_ids': "['sg', 'sg2']"
                    }
                ]
            }
        ]
        if sys.version_info[0] < 3:

            expected_result = [
                {
                    'failure_count': '0',
                    'filename': '/json/security_group/non_32_cidr.json',
                    'file_results': [
                        {
                            'id': 'W9',
                            'type': 'VIOLATION::WARNING',
                            'message': 'Security Groups found with ingress cidr that is not /32',
                            'logical_resource_ids': "['sg', 'sg2']"
                        }
                    ]
                }
            ]

            new_file_results = []

            for info in expected_result[0]['file_results']:
                print('info: ' + str(info))
                print('type: ' + str(type(info)))
                order_of_keys = ["id", "type", "message", "logical_resource_ids"]

                new_results = OrderedDict()
                for key in order_of_keys:
                    new_results[key] = info[key]

                new_file_results.append(new_results)
                print('new file results: ' + str(new_file_results))

                expected_result[0]['file_results'] = new_file_results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
            expected_result = [OrderedDict(list_of_tuples)]


        expected_result = pretty(expected_result)

        template_name = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + '/cloudformation_validator/test_templates/json/security_group/non_32_cidr.json'
        debug = False

        config_dict = {}
        config_dict['template_file'] = template_name
        config_dict['debug'] = debug
        config_dict['profile'] = None
        config_dict['rules_directory'] = None
        config_dict['input_path'] = None
        config_dict['profile'] = None
        config_dict['allow_suppression'] = False
        config_dict['print_suppression'] = False
        config_dict['parameter_values_path'] = None
        config_dict['isolate_custom_rule_exceptions'] = None
        validator = class_to_test(config_dict)

        real_result = validator.validate()
        self.maxDiff = None
        print('expected results: ' + str(expected_result))
        print('real results: ' + str(real_result))

        self.assertEqual(expected_result, real_result)

    def test_multiple_security_groups(self):

      expected_result = [
            {
                'failure_count': '0',
                'filename': '/json/security_group/multiple_ingress_security_groups.json',
                'file_results': [
                    {
                        'id': 'W5',
                        'type': 'VIOLATION::WARNING',
                        'message': 'Security Groups found with cidr open to world on egress',
                        'logical_resource_ids': "['emrSecurityGroup']"
                    }
                ]
            }
        ]

      if sys.version_info[0] < 3:
          new_file_results = []

          for info in expected_result[0]['file_results']:
              print('info: ' + str(info))
              print('type: ' + str(type(info)))
              order_of_keys = ["id", "type", "message", "logical_resource_ids"]

              new_results = OrderedDict()
              for key in order_of_keys:
                  new_results[key] = info[key]

              new_file_results.append(new_results)
              print('new file results: ' + str(new_file_results))

              expected_result[0]['file_results'] = new_file_results

          order_of_keys = ["failure_count", "filename", "file_results"]
          list_of_tuples = [(key, expected_result[0][key]) for key in order_of_keys]
          expected_result = [OrderedDict(list_of_tuples)]

      expected_result = pretty(expected_result)

      template_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/cloudformation_validator/test_templates/json/security_group/multiple_ingress_security_groups.json'
      debug = False

      config_dict = {}
      config_dict['template_file'] = template_name
      config_dict['debug'] = debug
      config_dict['profile']= None
      config_dict['rules_directory'] = None
      config_dict['input_path'] = None
      config_dict['profile'] = None
      config_dict['allow_suppression'] = False
      config_dict['print_suppression'] = False
      config_dict['parameter_values_path'] = None
      config_dict['isolate_custom_rule_exceptions'] = None
      validator = class_to_test(config_dict)

      real_result =  validator.validate()
      self.maxDiff = None

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.assertEqual(expected_result, real_result)

