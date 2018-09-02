import os
import sys
import unittest
from collections import OrderedDict
from cfn_model.model.EC2NetworkInterface import EC2NetworkInterface as class_to_test

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

class TestEc2Interface(unittest.TestCase):
    """
    Test ipaddr
    """

    def test_new_interface(self):


      cfn_model = {

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



      expected_result = 'EC2NetworkInterface'

      real_result = class_to_test(cfn_model=cfn_model)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))
      print('type: '+str(type(real_result)))
      print('name: '+str(real_result.__class__.__name__))
      self.maxDiff = None
      self.assertEqual(expected_result, real_result.__class__.__name__)

