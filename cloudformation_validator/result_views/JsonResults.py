
import inspect
import re
import sys
from builtins import (str)
from collections import OrderedDict

def lineno():
    """Returns the current line number in our program."""
    return str(' - JsonResults - line number: '+str(inspect.currentframe().f_back.f_lineno))

class JsonResults:

    def __init__(self, debug=False, suppress_errors=False):
        '''
        Initialize JsonResults
        :param debug:
        '''
        self.debug = debug
        self.suppress_errors = suppress_errors
        if self.debug:
            print('JsonResults - init'+lineno())

    def pretty(self, value, htchar='\t', lfchar='\n', indent=0):
        '''
        Prints pretty json
        :param value:
        :param htchar:
        :param lfchar:
        :param indent:
        :return: pretty json
        '''

        if self.debug:
            print('### type: '+str(type(value))+lineno())
            if type(value) == type(OrderedDict()):
                print('found it')

        nlch = lfchar + htchar * (indent + 1)
        if type(value) == type(dict()) or type(value) == type(OrderedDict()):
            if (self.debug):
                print('is dict')
            items = [
                nlch + repr(key) + ': ' + self.pretty(value[key], htchar, lfchar, indent + 1)
                for key in value
            ]
            return '{%s}' % (','.join(items) + lfchar + htchar * indent)
        elif type(value) == type(list()):
            if (self.debug):
                print('is list')
            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in value
            ]
            return '[%s]' % (','.join(items) + lfchar + htchar * indent)
        elif type(value) is tuple:
            if (self.debug):
                print('is tuple')
            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in value
            ]
            return '(%s)' % (','.join(items) + lfchar + htchar * indent)
        else:
            if (self.debug):
                print('is other')
            return repr(value)


    def render(self, results):
        '''
        Renders results
        :param results:
        :return:
        '''
        if self.debug:
            print('render:'+lineno())

            print('results: '+str(results)+lineno())
            print('type: '+str(type(results))+lineno())



        if type(results)==type(list()):

            if self.debug:
                print('is a list: '+lineno())

            for r in results:
                if self.debug:
                    print('r: '+str(r)+lineno())

                if 'filename' in r:

                    if self.debug:
                        print('r: '+str(r)+lineno())
                        print('filename: '+str(r['filename'])+lineno())

                    matchObj = re.match(r'(.*)(/json.*)', r['filename'], re.M | re.I)

                    if matchObj:
                        r['filename'] = matchObj.group(2)
                    else:
                        if self.debug:
                            print("No match!!")

                if 'file_results' in r:
                    new_violations = []

                    if 'failure_count' in r['file_results']:
                        r['file_results'].pop('failure_count', None)


                    if 'violations' in r['file_results']:

                        if self.debug:
                            print('found violations: '+lineno())
                            print('type: '+str(type(r['file_results']['violations']))+lineno())

                        if type(r['file_results']['violations']) == type(list()):

                            if self.debug:
                                print('is a list'+lineno())

                            for violation in r['file_results']['violations']:

                                if self.debug:
                                    print('violation: '+str(violation))
                                    print('type: '+str(type(violation))+lineno())

                                new_violations.append(violation.to_hash())

                        elif type(r['file_results']['violations']) == type(dict()):
                            if self.debug:
                                print('is a dict'+lineno())
                            new_violations.append((r['file_results']))

                    else:
                        if self.debug:
                            print('type:'+str(r['file_results'])+lineno())
                        for item in r['file_results']:
                            if self.debug:
                                print(str(item.to_hash())+lineno())

                            new_violations.append(item.to_hash())

                    r['file_results'] = new_violations

            hash = results

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, hash[0][key]) for key in order_of_keys]
            hash= OrderedDict(list_of_tuples)


        else:

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, results[key]) for key in order_of_keys]
            new_results = OrderedDict(list_of_tuples)


            hash=[]
            for result in new_results:
                if self.debug:
                    print('result: '+str(result)+lineno())

                for item in result:

                    if item:
                        hash.append(item.to_hash())

        if self.debug:
            print('returning: '+str(hash)+lineno())

        return self.pretty(hash)