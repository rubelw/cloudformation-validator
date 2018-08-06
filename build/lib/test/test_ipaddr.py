import os
import sys
import unittest
from collections import OrderedDict
from cloudformation_validator.IpAddr import IpAddr as class_to_test

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

class TestIpAddr(unittest.TestCase):
    """
    Test ipaddr
    """

    def test_ip4_open(self):


      expected_result = True


      dict = {}
      dict['CidrIp'] = '0.0.0.0/0'

      real_result = class_to_test.ip4_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip4_open_list(self):


      expected_result = True


      dict = []
      dict.append({'CidrIp': '0.0.0.0/0'})

      real_result = class_to_test.ip4_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip4_not_open(self):


      expected_result = False


      dict = {}
      dict['CidrIp'] = '192.168.1.0/32'

      real_result = class_to_test.ip4_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip4_not_open_list(self):


      expected_result = False


      dict = []
      dict.append({'CidrIp':'192.168.1.0/32'})

      real_result = class_to_test.ip4_open(ingress=dict, debug=True)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)



    def test_ip6_open(self):


      expected_result = True


      dict = {}
      dict['CidrIp'] = '::/0'

      real_result = class_to_test.ip6_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)



    def test_ip6_open_list(self):


      expected_result = True


      dict = []
      dict.append({'CidrIp':'::/0'})

      real_result = class_to_test.ip6_open(ingress=dict, debug=True)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip6_not_open(self):


      expected_result = False


      dict = {}
      dict['CidrIp'] = '::/32'

      real_result = class_to_test.ip6_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip6_not_open_list(self):


      expected_result = False


      dict = []
      dict.append({'CidrIp': '::/32'})

      real_result = class_to_test.ip6_open(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)



    def test_ip4_no_range(self):


      expected_result = True


      dict = {}
      dict['CidrIp'] = '192.168.1.0/32'

      real_result = class_to_test.ip4_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)

    def test_ip4_range(self):


      expected_result = False


      dict = {}
      dict['CidrIp'] = '192.168.1.0/64'

      real_result = class_to_test.ip4_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip4_range_list(self):


      expected_result = False


      dict = []
      dict.append( {'CidrIp':'192.168.1.0/64'})

      real_result = class_to_test.ip4_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)



    def test_ip6_no_range(self):


      expected_result = True


      dict = {}
      dict['CidrIp'] = '2001:0db8:85a3:0000:0000:8a2e:0370/128'

      real_result = class_to_test.ip6_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)


    def test_ip6_range(self):


      expected_result = False


      dict = {}
      dict['CidrIp'] = '2001:0db8:85a3:0000:0000:8a2e:0370/64'

      real_result = class_to_test.ip6_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)

    def test_ip6_range_list(self):


      expected_result = False


      dict = []
      dict.append({'CidrIp': '2001:0db8:85a3:0000:0000:8a2e:0370/64'})

      real_result = class_to_test.ip6_cidr_range(ingress=dict, debug=False)

      print('expected results: '+str(expected_result))
      print('real results: '+str(real_result))

      self.maxDiff = None
      self.assertEqual(expected_result, real_result)