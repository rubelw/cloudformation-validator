import os
import sys
import unittest
from collections import OrderedDict
from cfn_model.model.References import References as class_to_test
from cfn_model.model.CfnModel import CfnModel

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

class TestReferencesModel(unittest.TestCase):
    """
    Test ipaddr
    """

    def test_references(self):


      cfn_model = {
          "Parameters": {
              "test": {
                  "Type": "String",
                  "Default": "subnet-4fd01116"
              }
          },
          "Resources": {
              "myENI": {
                  "Type": "AWS::EC2::NetworkInterface",
                  "Properties": {
                      "Tags": [{"Key": "foo", "Value": "bar"}],
                      "Description": "A nice description.",
                      "SourceDestCheck": "false",
                      "GroupSet": ["sg-75zzz219"],
                      "SubnetId": "subnet-3z648z53",
                      "PrivateIpAddress": "10.0.0.16"
                  }
              }
          }
        }

      model = CfnModel()
      model.raw_model = cfn_model
      model.transform_hash_into_parameters(cfn_model)

      value={"Ref":"test"}

      expected_result = {"Ref":"test"}

      real_result = class_to_test.resolve_value(cfn_model=model, value=value, debug=True)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))
      print('type: '+str(type(real_result)))
      print('name: '+str(real_result.__class__.__name__))
      self.maxDiff = None
      self.assertEqual(expected_result, real_result)

