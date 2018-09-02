from __future__ import absolute_import, division, print_function
import inspect
import sys

def lineno():
    """Returns the current line number in our program."""
    return str(' - IpAddr - line number: '+str(inspect.currentframe().f_back.f_lineno))


class IpAddr:
    """
    Ip address
    """
    @staticmethod
    def ip4_open(ingress, debug=False):
        """
        Whether ip4 is open to the world
        :param debug:
        :return: boolean
        """
        if debug:
            print('ip4_open'+lineno())
            print("\ningress: "+str(ingress)+lineno())
            if hasattr(ingress,'__dict__'):
                print('vars: '+str(vars(ingress))+lineno())
                if inspect.isclass(ingress):
                    print(str(vars(ingress)))

        if type(ingress)== type(dict()):
            if debug:
                print("\ningress is a dict"+lineno())
            if ingress['CidrIp'] == '0.0.0.0/0':
                return True

        elif type(ingress) == type(list()):
            if debug:
                print("ingress is a list"+lineno())
            for item in ingress:

                if debug:
                    print('item is: '+str(item)+lineno())

                if 'CidrIp' in item and item['CidrIp'] == '0.0.0.0/0':
                    return True

        elif hasattr(ingress, 'cfn_model'):
            if debug:
              print('ingress is object and has cfn_model attribute'+lineno())

            if hasattr(ingress.cfn_model, 'cfn_model'):
                if debug:
                    print("\ningress cfn_model object has a cfn_model"+lineno())

                if type(ingress.cfn_model.cfn_model) == type(dict()):

                    if ingress.cfn_model.cfn_model['CidrIp'] == '0.0.0.0/0':
                        return True

                elif type(ingress.cfn_model.cfn_model) == type(list()):
                    for item in ingress.cfn_model.cfn_model:
                        if item == 'CidrIp' and item['CidrIp'] == '0.0.0.0/0':
                            return True

            elif hasattr(ingress, 'cidrIp'):
                if debug:
                    print("\ningress had cidrIp attribute"+lineno())
                if type(ingress.cidrIp) == type(str()) and str(ingress.cidrIp) == '0.0.0.0/0':
                    return True

                if sys.version_info[0] < 3:
                    if type(ingress.cidrIp) == type(unicode()) and str(ingress.cidrIp) == '0.0.0.0/0':
                        return True

            else:
                if debug:
                    print("\n"+str(ingress.cfn_model)+lineno())

                if type(ingress.cfn_model) == type(dict()):
                    if debug:
                        print("\ningress cfn model is a dict"+lineno())

                    if 'Properties' in ingress.cfn_model:
                        if 'CidrIp' in ingress.cfn_model['Properties']:
                            if type(ingress.cfn_model['Properties']['CidrIp']) == type(str()) and str(
                                  ingress.cfn_model['Properties']['CidrIp']) == '0.0.0.0/0':
                                return True

                            if sys.version_info[0] < 3:
                                if type(ingress.cfn_model['Properties']['CidrIp']) == type(unicode()) and str(
                                      ingress.cfn_model['Properties']['CidrIp']) == '0.0.0.0/0':
                                    return True

                elif type(ingress.cfn_model)== type(list()):
                    if debug:
                        print("\ningress is a list"+lineno())

                    for item in ingress.cfn_model:
                        if debug:
                            print(str(item)+lineno())

                else:
                    if debug:
                        print(str(vars(ingress.cfn_model))+lineno())

                    if hasattr(ingress.cfn_model,'cfn_model'):
                        if debug:
                            print(str(ingress.cfn_model.cfn_model)+lineno())
                        if 'Properties' in ingress.cfn_model.cfn_model:
                            if 'CidrIp' in ingress.cfn_model['Properties']:
                                if type(ingress.cfn_model.cfn_model['Properties']['CidrIp']) == type(str()) and str(
                                        ingress.cfn_model.cfn_model['Properties']['CidrIp']) == '0.0.0.0/0':
                                    return True

                                if sys.version_info[0] < 3:
                                    if type(ingress.cfn_model.cfn_model['Properties']['CidrIp']) == type(unicode()) and str(
                                            ingress.cfn_model.cfn_model['Properties']['CidrIp']) == '0.0.0.0/0':
                                        return True

                    elif type(ingress) == type(dict()):
                        if debug:
                            print('is a dict'+lineno())

                        if ingress['CidrIp'] == '0.0.0.0/0':
                            return True

                    elif type(ingress) == type(list()):

                        if debug:
                            print('is a list'+lineno())

                        for item in ingress:
                            if item == 'CidrIp' and item['CidrIp'] == '0.0.0.0/0':
                                return True

        return False

    @staticmethod
    def ip6_open(ingress, debug=False):
        """
        if ipv6 is open to world
        :param debug:
        :return: boolean
        """
        if debug:
            print('ip6_open'+lineno())
            print('ingress: '+str(ingress)+lineno())
            if hasattr(ingress,'__dict__'):
                print('vars: '+str(vars(ingress))+lineno())


        if type(ingress)==type(dict()):
            if ingress['CidrIp'] == '::/0':
                return True

        elif type(ingress) == type(list()):

            for item in ingress:
                if 'CidrIp' in item and item['CidrIp'] == '::/0':
                    return True

        elif hasattr(ingress,'cfn_model'):
            if debug:
                print('ingress is object and has cfn_model attribute'+lineno())

            if hasattr(ingress.cfn_model, 'cfn_model'):
                if debug:
                    print("\ningress cfn_model object has a cfn_model"+lineno())
                if type(ingress.cfn_model.cfn_model) == type(dict()):

                    if ingress.cfn_model.cfn_model['CidrIp'] == '::/0':
                        return True

                elif type(ingress.cfn_model.cfn_model) == type(list()):

                    for item in ingress.cfn_model.cfn_model:
                        if item == 'CidrIp' and item['CidrIp'] == '::/0':
                            return True
        else:
            if debug:
                print('var:' + str(vars(ingress)) + lineno())

            if hasattr(ingress,'cidrIp'):
                if type(ingress.cidrIp) == type(str()) and str(ingress.cidrIp) == '::/0':
                    return True

                if sys.version_info[0] < 3:
                    if type(ingress.cidrIp) == type(unicode()) and str(ingress.cidrIp) == '::/0':
                        return True

            elif hasattr(ingress,'cidrIpv6'):

                if type(ingress.cidrIpv6) == type(str()) and str(ingress.cidrIpv6) == '::/0':
                    return True

                if sys.version_info[0] < 3:
                    if type(ingress.cidrIpv6) == type(unicode()) and str(ingress.cidrIpv6) == '::/0':
                        return True

            elif hasattr(ingress, 'cfn_model'):

                if 'Properties' in ingress.cfn_model:
                    if 'CidrIp' in ingress.cfn_model['Properties']:
                        if type(ingress.cfn_model['Properties']['CidrIp']) == type(str()) and str(ingress.cfn_model['Properties']['CidrIp']) == '::/0':
                            return True

                        if sys.version_info[0] < 3:
                            if type(ingress.cfn_model['Properties']['CidrIp']) == type(unicode()) and str(ingress.cfn_model['Properties']['CidrIp']) == '::/0':
                                return True

        return False

    @staticmethod
    def ip4_cidr_range(ingress, debug=False):
        """
        IP4 is not /32
        :param debug:
        :return: boolean
        """
        if debug:
            print('ip4_cidr_range '+str(ingress)+lineno())
            print('type: '+str(type(ingress))+lineno())

        suffix = "/32";

        if type(ingress)==type(dict()):

            if debug:
                print('ingress is a dict: '+lineno())

            if 'CidrIp' in ingress:

                if debug:
                    print('CidrIp in ingress '+lineno())
                    print('type: '+str(type(ingress['CidrIp']))+lineno())

                if type(ingress['CidrIp']) == type(str()):

                    if debug:
                        print('ip is: ' + str(ingress['CidrIp']) + lineno())

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress['CidrIp']:
                        return True

                    elif ingress['CidrIp'].endswith(suffix):

                        if debug:
                            print('ip ends with /32' + lineno())

                        return True
                    else:
                        if debug:
                            print('ip does not end with /32'+lineno())
                        return False

                if sys.version_info[0] < 3 and type(ingress['CidrIp']) == type(unicode()):

                    if debug:
                        print('ip is: ' + str(ingress['CidrIp']) + lineno())

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress['CidrIp']:
                        return True

                    elif ingress['CidrIp'].endswith(suffix):

                        if debug:
                            print('ip ends with /32' + lineno())

                        return True
                    else:
                        if debug:
                            print('ip does not end with /32'+lineno())
                        return False

        elif type(ingress) == type(list()):
            if debug:
                print('is a list: '+lineno())

            for item in ingress:
                if 'CidrIp' in item:
                    if type(item['CidrIp']) == type(str()):

                        if debug:
                            print('ip is: ' + str(item['CidrIp']) + lineno())

                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in item['CidrIp']:
                            return True

                        elif item['CidrIp'].endswith(suffix):
                            if debug:
                                print('ip ends with /32' + lineno())
                            return True
                        else:
                            if debug:
                                print('ip does not end with /32'+lineno())
                            return False

                    if sys.version_info[0] < 3 and type(item['CidrIp']) == type(unicode()):

                            if debug:
                                print('ip is: ' + str(item['CidrIp']) + lineno())

                            # only care about literals.  if a Hash/Ref not going to chase it down
                            # given likely a Parameter with external val
                            if 'Ref' in item['CidrIp']:
                                return True

                            elif item ['CidrIp'].endswith(suffix):
                                if debug:
                                    print('ip ends with /32' + lineno())
                                return True
                            else:
                                if debug:
                                    print('ip does not end with /32'+lineno())
                                return False


        elif hasattr(ingress,'cidrIp'):

            if type(ingress.cidrIp) == type(str()):

                if debug:
                    print('ip is: '+str(ingress.cidrIp)+lineno())

                if type(ingress.cidrIp) == type(list()):

                    for item in ingress:
                        if 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    return True

                                elif item['CidrIp'].endswith(suffix):

                                    if debug:
                                        print('ip ends with /32' + lineno())

                                    return True

                                else:
                                    if debug:
                                        print('ip does not end with /32' + lineno())
                                    return False

                            if sys.version_info[0] < 3 and type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        return True

                                    elif item['CidrIp'].endswith(suffix):

                                        if debug:
                                            print('ip ends with /32' + lineno())

                                        return True

                                    else:
                                        if debug:
                                            print('ip does not end with /32' + lineno())
                                        return False


                elif type(ingress.cidrIp) == type(dict()):

                    for item in ingress.cidrIp:
                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress.cidrIp[item]:
                            return True

                        elif item == 'Ref':
                            return True

                        elif ingress.cidrIp[item].endswith(suffix):
                            if debug:
                                print('ip ends with /32' + lineno())
                            return True

                        else:
                            if debug:
                                print('ip does not end with /32'+lineno())
                            return False

                elif type(ingress.cidrIp) == type(str()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIp:
                        return True

                    elif ingress.cidrIp.endswith(suffix):
                        if debug:
                            print('ip ends with /32' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /32' + lineno())
                        return False

                elif sys.version_info[0] < 3 and  type(ingress.cidrIp) == type(unicode()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIp:
                        return True

                    elif ingress.cidrIp.endswith(suffix):
                        if debug:
                            print('ip ends with /32' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /32' + lineno())
                        return False
                else:
                    print('not sure what this is')
                    print('need to fix')
                    sys.exit(1)

            elif sys.version_info[0] < 3 and type(ingress.cidrIp) == type(unicode()):

                if debug:
                    print('ip is: '+str(ingress.cidrIp)+lineno())

                if type(ingress.cidrIp) == type(list()):

                    for item in ingress:
                        if 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    return True

                                elif item['CidrIp'].endswith(suffix):

                                    if debug:
                                        print('ip ends with /32' + lineno())

                                    return True

                                else:
                                    if debug:
                                        print('ip does not end with /32' + lineno())
                                    return False

                            if sys.version_info[0] < 3:
                                if type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        return True

                                    elif item['CidrIp'].endswith(suffix):

                                        if debug:
                                            print('ip ends with /32' + lineno())

                                        return True

                                    else:
                                        if debug:
                                            print('ip does not end with /32' + lineno())
                                        return False

                elif type(ingress.cidrIp) == type(dict()):

                    for item in ingress.cidrIp:
                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress.cidrIp[item]:
                            return True

                        elif item == 'Ref':
                            return True

                        elif ingress.cidrIp[item].endswith(suffix):
                            if debug:
                                print('ip ends with /32' + lineno())
                            return True

                        else:
                            if debug:
                                print('ip does not end with /32'+lineno())
                            return False

                elif type(ingress.cidrIp) == type(str()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIp:
                        return True

                    elif ingress.cidrIp.endswith(suffix):
                        if debug:
                            print('ip ends with /32' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /32' + lineno())
                        return False

                elif sys.version_info[0] < 3 and type(ingress.cidrIp) == type(unicode()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIp:
                        return True

                    elif ingress.cidrIp.endswith(suffix):
                        if debug:
                            print('ip ends with /32' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /32' + lineno())
                        return False
                else:
                    print('not sure what this is')
                    print('need to fix')
                    sys.exit(1)

            else:

                if debug:
                    print('ip is: ' + str(ingress.cidrIp) + lineno())
                    print('type: '+str(type(ingress.cidrIp))+lineno())

                if type(ingress.cidrIp) == type(dict()):

                    if debug:
                        print('is a dict: '+lineno())

                    for item in ingress.cidrIp:

                        if debug:
                            print('item: '+str(item)+lineno())

                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress.cidrIp[item]:
                            if debug:
                                print('is a ref - ignoring = '+lineno())
                            return True

                        elif item == 'Ref':
                            if debug:
                                print('is a ref - ignoring - '+lineno())
                            return True

                        elif ingress.cidrIp[item].endswith(suffix):
                            if debug:
                                print('ip ends with /32' + lineno())
                            return True

                        else:
                            if debug:
                                print('ip does not end with /32'+lineno())
                            return False

                elif type(ingress.cidrIp) == type(list()):

                    if debug:
                      print('is a list: '+lineno())

                    has_invalid_cidr = False

                    for item in ingress.cidrIp:

                        if debug:
                            print('list item: '+str(item)+lineno())


                        if type(item) == type(dict()):

                            for item2 in item:

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item[item2]:
                                    return True

                                elif item2 == 'Ref':
                                    return True

                                elif item[item2].endswith(suffix):
                                    if debug:
                                        print('ip ends with /32' + lineno())
                                    return True

                                else:
                                    if debug:
                                        print('ip does not end with /32' + lineno())
                                    return False

                        elif 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    has_invalid_cidr= True

                                elif item['CidrIp'].endswith(suffix):
                                    if debug:
                                        print('ip ends with /32' + lineno())
                                    return True
                                else:
                                    if debug:
                                        print('ip does not end with /32' + lineno())
                                    has_invalid_cidr= False

                            if sys.version_info[0] < 3 and type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        has_invalid_cidr= True

                                    elif item['CidrIp'].endswith(suffix):
                                        if debug:
                                            print('ip ends with /32' + lineno())
                                        return True
                                    else:
                                        if debug:
                                            print('ip does not end with /32' + lineno())
                                        has_invalid_cidr= False

                        return has_invalid_cidr

                else:
                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIp:
                        return True

                    elif ingress.cidrIp.endswith(suffix):
                        if debug:
                            print('ip ends with /32' + lineno())
                        return True

                    else:
                        if debug:
                            print('ip does not end with /32'+lineno())
                        return False

        elif type(ingress) == type(str()):
            if debug:
                print('is a str '+lineno())


            # only care about literals.  if a Hash/Ref not going to chase it down
            # given likely a Parameter with external val
            if 'Ref' in ingress:
                return True

            elif ingress.endswith('/32'):
                return True
            else:
                if debug:
                    print('ip does not end with /32' + lineno())
                return False
        elif sys.version_info[0] < 3 and type(ingress) == type(unicode()):
            if debug:
                print('is a str '+lineno())


            # only care about literals.  if a Hash/Ref not going to chase it down
            # given likely a Parameter with external val
            if 'Ref' in ingress:
                return True

            elif ingress.endswith('/32'):
                return True
            else:
                if debug:
                    print('ip does not end with /32' + lineno())
                return False
        else:

            print('not sure what type of object this is '+lineno())
            print('vars: '+str(vars(ingress))+lineno())
            sys.exit(1)

        return False

        #ingress.cidrIp.is_a?(String) && !ingress.cidrIp.end_with?('/32')

    @staticmethod
    def ip6_cidr_range(ingress, debug=False):
        """
        If ipv6 is not /128
        :param debug:
        :return: boolean
        """
        if debug:
              print('ip6_cidr_range ' + str(ingress) + lineno())
              print('type: ' + str(type(ingress)) + lineno())
              if hasattr(ingress, '__dict__'):
                  print('vars: ' + str(vars(ingress)) + lineno())

        suffix = "/128";

        if type(ingress) == type(dict()):

            if debug:
                print('ingress is a dict: ' + lineno())

            if 'CidrIp' in ingress:

                if debug:
                    print('CiderIp in ingress '+lineno())

                if type(ingress['CidrIp']) == type(str()):

                    if debug:
                        print('ip is: ' + str(ingress['CidrIp']) + lineno())

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress['CidrIp']:
                        return True

                    elif ingress['CidrIp'].endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False

                elif sys.version_info[0] < 3 and  type(ingress['CidrIp']) == type(unicode()):

                        if debug:
                            print('ip is: ' + str(ingress['CidrIp']) + lineno())

                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress['CidrIp']:
                            return True

                        elif ingress['CidrIp'].endswith(suffix):
                            if debug:
                                print('ip ends with /128' + lineno())
                            return True
                        else:
                            if debug:
                                print('ip does not end with /128' + lineno())
                            return False

        elif type(ingress) == type(list()):

            for item in ingress:
                if 'CidrIp' in item:
                    if type(item['CidrIp']) == type(str()):

                        if debug:
                            print('ip is: ' + str(item['CidrIp']) + lineno())

                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in item['CidrIp']:
                            return True

                        elif item['CidrIp'].endswith(suffix):
                            if debug:
                                print('ip ends with /128' + lineno())
                            return True
                        else:
                            if debug:
                                print('ip does not end with /128' + lineno())
                            return False

                    if sys.version_info[0] < 3 and  type(item['CidrIp']) == type(unicode()):

                            if debug:
                                print('ip is: ' + str(item['CidrIp']) + lineno())

                            # only care about literals.  if a Hash/Ref not going to chase it down
                            # given likely a Parameter with external val
                            if 'Ref' in item['CidrIp']:
                                return True

                            elif item['CidrIp'].endswith(suffix):
                                if debug:
                                    print('ip ends with /128' + lineno())
                                return True
                            else:
                                if debug:
                                    print('ip does not end with /128' + lineno())
                                return False

        elif hasattr(ingress, 'cidrIpv6'):

            if type(ingress.cidrIpv6) == type(str()):

                if debug:
                    print('ip is: ' + str(ingress.cidrIpv6) + lineno())

                if type(ingress.cidrIpv6) == type(list()):

                    for item in ingress:
                        if 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    return True

                                elif item['CidrIp'].endswith(suffix):
                                    if debug:
                                        print('ip ends with /128' + lineno())
                                    return True
                                else:
                                    if debug:
                                        print('ip does not end with /128' + lineno())
                                    return False
                            if sys.version_info[0] < 3:
                                if type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        return True

                                    elif item['CidrIp'].endswith(suffix):
                                        if debug:
                                            print('ip ends with /128' + lineno())
                                        return True
                                    else:
                                        if debug:
                                            print('ip does not end with /128' + lineno())
                                        return False

                elif type(ingress.cidrIpv6) == type(dict()):

                    for item in ingress.cidrIp:
                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress.cidrIpv6[item]:
                            return True

                        elif ingress.cidrIpv6[item].endswith(suffix):
                            if debug:
                                print('ip ends with /128' + lineno())
                            return True

                        else:
                            if debug:
                                print('ip does not end with /128' + lineno())
                            return False
                elif type(ingress.cidrIpv6) == type(str()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIpv6:
                        return False

                    elif ingress.cidrIpv6.endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False

                elif sys.version_info[0] < 3 and type(ingress.cidrIpv6) == type(unicode()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIpv6:
                        return False

                    elif ingress.cidrIpv6.endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False
                else:
                    print('not sure what this is')
                    print('need to fix')
                    sys.exit(1)

            elif sys.version_info[0] < 3 and type(ingress.cidrIpv6) == type(unicode()):

                if debug:
                    print('ip is: ' + str(ingress.cidrIpv6) + lineno())

                if type(ingress.cidrIpv6) == type(list()):

                    for item in ingress:
                        if 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    return True

                                elif item['CidrIp'].endswith(suffix):
                                    if debug:
                                        print('ip ends with /128' + lineno())
                                    return True
                                else:
                                    if debug:
                                        print('ip does not end with /128' + lineno())
                                    return False
                            if sys.version_info[0] < 3:
                                if type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        return True

                                    elif item['CidrIp'].endswith(suffix):
                                        if debug:
                                            print('ip ends with /128' + lineno())
                                        return True
                                    else:
                                        if debug:
                                            print('ip does not end with /128' + lineno())
                                        return False

                elif type(ingress.cidrIpv6) == type(dict()):

                    for item in ingress.cidrIp:
                        # only care about literals.  if a Hash/Ref not going to chase it down
                        # given likely a Parameter with external val
                        if 'Ref' in ingress.cidrIpv6[item]:
                            return True

                        elif ingress.cidrIpv6[item].endswith(suffix):
                            if debug:
                                print('ip ends with /128' + lineno())
                            return True

                        else:
                            if debug:
                                print('ip does not end with /128' + lineno())
                            return False
                elif type(ingress.cidrIpv6) == type(str()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIpv6:
                        return False

                    elif ingress.cidrIpv6.endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False

                elif sys.version_info[0] < 3 and type(ingress.cidrIpv6) == type(unicode()):

                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIpv6:
                        return False

                    elif ingress.cidrIpv6.endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True
                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False
                else:
                    print('not sure what this is')
                    print('need to fix')
                    sys.exit(1)

            else:
                if debug:
                    print('ip is: ' + str(ingress.cidrIpv6) + lineno())
                    print('type: ' + str(type(ingress.cidrIpv6)) + lineno())

                if type(ingress.cidrIpv6) == type(list()):

                    has_invalid_cidr = False

                    for item in ingress.cidrIpv6:

                        if debug:
                            print('list item: ' + str(item) + lineno())

                        if type(item) == type(dict()):

                            for item2 in item:
                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item[item2]:
                                    return True

                                elif item2 == 'Ref':
                                    return True

                                elif item[item2].endswith(suffix):
                                    if debug:
                                        print('ip ends with /32' + lineno())
                                    return True

                                else:
                                    if debug:
                                        print('ip does not end with /32' + lineno())
                                    return False

                        elif 'CidrIp' in item:
                            if type(item['CidrIp']) == type(str()):

                                if debug:
                                    print('ip is: ' + str(item['CidrIp']) + lineno())

                                # only care about literals.  if a Hash/Ref not going to chase it down
                                # given likely a Parameter with external val
                                if 'Ref' in item['CidrIp']:
                                    has_invalid_cidr = True

                                elif item['CidrIp'].endswith(suffix):
                                    if debug:
                                        print('ip ends with /128' + lineno())
                                    return True
                                else:
                                    if debug:
                                        print('ip does not end with /128' + lineno())
                                    has_invalid_cidr = False

                            if sys.version_info[0] < 3:
                                if type(item['CidrIp']) == type(unicode()):

                                    if debug:
                                        print('ip is: ' + str(item['CidrIp']) + lineno())

                                    # only care about literals.  if a Hash/Ref not going to chase it down
                                    # given likely a Parameter with external val
                                    if 'Ref' in item['CidrIp']:
                                        has_invalid_cidr = True

                                    elif item['CidrIp'].endswith(suffix):
                                        if debug:
                                            print('ip ends with /128' + lineno())
                                        return True
                                    else:
                                        if debug:
                                            print('ip does not end with /128' + lineno())
                                        has_invalid_cidr = False

                        return has_invalid_cidr

                else:
                    # only care about literals.  if a Hash/Ref not going to chase it down
                    # given likely a Parameter with external val
                    if 'Ref' in ingress.cidrIpv6:
                        return True

                    elif ingress.cidrIpv6.endswith(suffix):
                        if debug:
                            print('ip ends with /128' + lineno())
                        return True

                    else:
                        if debug:
                            print('ip does not end with /128' + lineno())
                        return False

        elif type(ingress) == type(str()):
            if debug:
                print('is a str ' + lineno())

            # only care about literals.  if a Hash/Ref not going to chase it down
            # given likely a Parameter with external val
            if 'Ref' in ingress:
                return True

            elif ingress.endswith('/128'):
                return True
            else:
                if debug:
                    print('ip does not end with /128' + lineno())
                return False
        elif sys.version_info[0] < 3 and type(ingress) == type(unicode()):
            if debug:
                print('is a str ' + lineno())

            # only care about literals.  if a Hash/Ref not going to chase it down
            # given likely a Parameter with external val
            if 'Ref' in ingress:
                return True

            elif ingress.endswith('/128'):
                return True
            else:
                if debug:
                    print('ip does not end with /128' + lineno())
                return False

        return False