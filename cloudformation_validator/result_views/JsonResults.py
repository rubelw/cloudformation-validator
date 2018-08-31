from __future__ import absolute_import, division, print_function
from future.types.newstr import newstr
import inspect
import re
import sys
import json
import os
from builtins import (str)
from collections import OrderedDict
from cloudformation_validator.Violation import Violation

def lineno():
    """Returns the current line number in our program."""
    return str(' - JsonResults - line number: '+str(inspect.currentframe().f_back.f_lineno))

class JsonResults:
    """
    Json results
    """
    def __init__(self, debug=False, suppress_errors=False):
        """
        Initialize JsonResults
        :param debug:
        """
        self.debug = debug
        self.suppress_errors = suppress_errors
        if self.debug:
            print('JsonResults - init'+lineno())



    def pretty(self, value, htchar='\t', lfchar='\n', indent=0):
        """
        Prints pretty json
        :param value:
        :param htchar:
        :param lfchar:
        :param indent:
        :return: pretty json
        """

        if self.debug:
            print('### type: '+str(type(value))+lineno()+lineno())
        if type(value) == type(OrderedDict()):
            if self.debug:
                print('found it'+lineno())
                print('value: '+str(value)+lineno())


        nlch = lfchar + htchar * (indent + 1)
        if type(value) == type(dict()) or type(value) == type(OrderedDict()):
            if (self.debug):
                print("##############################\n")
                print('is dict'+lineno())
                print("##############################\n")

            items = [
                nlch + repr(key) + ': ' + self.pretty(value[key], htchar, lfchar, indent + 1)
                for key in value
            ]
            return str('{%s}' % (','.join(items) + lfchar + htchar * indent)).replace('\'','"').replace(']"',']').replace('"[','[').replace('"{"','{"').replace('"}"','"}').replace('"[\'','[\'').replace('\']"','\']')

        elif type(value) == type(list()):
            if (self.debug):
                print("##############################\n")
                print('is list'+lineno())
                print("##############################\n")


            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in value
            ]
            if self.debug:
                print('items: '+str(items)+lineno())
                print('items type: '+str(type(items))+lineno())
            if items:
                items = sorted(items)
            [str(item) for item in sorted(items)]
            return str('[%s]' % (','.join(sorted(items)) + lfchar + htchar * indent)).replace('\'','"').replace(']"',']').replace('"[','[').replace('"{"','{"').replace('"}"','"}').replace('"[\'','[\'').replace('\']"','\']')

        elif type(value) is tuple:
            if (self.debug):
                print("##############################\n")
                print('is tuple'+lineno())
                print("##############################\n")

            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in sorted(value)
            ]

            if self.debug:
                print('returning: '+str('(%s)' % (','.join(items) + lfchar + htchar * indent))+lineno())
            return str('(%s)' % (','.join(items) + lfchar + htchar * indent)).replace('\'','"').replace(']"',']').replace('"[','[').replace('"{"','{"').replace('"}"','"}').replace('"[\'','[\'').replace('\']"','\']')

        elif type(value) == type(newstr()):
            if self.debug:
                print('is a new string'+lineno())
                print('value: '+str(value)+lineno())

            if value.startswith('['):
                if self.debug:
                    print('starts with bracket'+lineno())
                my_json = eval((value.replace('\'','"')))
                my_new_list = []
                for my_it in sorted(my_json):
                    my_new_list.append(str(my_it))
                return str('"'+str(my_new_list)+'"').replace(']"',']').replace('"[','[').replace('"{"','{"').replace('"}"','"}').replace('"[\'','[\'').replace('\']"','\']')
                #value = self.pretty(my_json, htchar, lfchar, indent + 1)



            return repr(str(value))

        else:
            if (self.debug):
                print("##############################\n")
                print('is other: '+str(type(value))+lineno())
                print('class name: '+str(value.__class__.__name__))
                print('returning: '+str(value))
                print("##############################\n")

            return str(repr(str(value))).replace('\'','"').replace(']"',']').replace('"[','[').replace('"{"','{"').replace('"}"','"}').replace('"[\'','[\'').replace('\']"','\']')


    def render(self, results):
        """
        Renders results
        :param results:
        :return:
        """
        if self.debug:
            print("########################################")
            print('render:'+lineno())

            print('results: '+str(results)+lineno())
            print('type: '+str(type(results))+lineno())
            print("#########################################\n")
        array_of_results = []

        # This is an array of violations
        if type(results)==type(list()):

            if self.debug:
                print('is a list: '+lineno())
                print('list count: '+str(len(results))+lineno())

            ordered_violations_by_filename = {}

            # Iterate over each of the violqtions
            for r in results:
                if self.debug:

                    print("\n"+'################################')
                    print('violation: '+str(r)+lineno())
                    print('###################################'+"\n")

                # Not doing anything
                if 'filename' in r:

                    if self.debug:
                        print('r: '+str(r)+lineno())
                        print('filename: '+str(r['filename'])+lineno())

                    matchObj = re.match(r'(.*)(/json.*)', r['filename'], re.M | re.I)

                    if matchObj:
                        r['filename'] = matchObj.group(2)
                    else:
                        if self.debug:
                            print('no match '+lineno())


                # Not doing anything
                if 'file_results' in r:
                    if self.debug:
                        print('threre are file results: '+str(r['file_results'])+lineno())

                    if 'failure_count' in r['file_results']:
                        r['file_results'].pop('failure_count', None)

                new_violations_list = []
                # If there are violations in the file results
                # Lets put the violations in to an OrderedDict
                if 'violations' in r['file_results']:

                    if self.debug:
                        print('found violations: '+lineno())
                        print('type: '+str(type(r['file_results']['violations']))+lineno())

                    # Lets first just iterate over the violations and get the id so
                    # we can sort
                    if type(r['file_results']['violations']) == type(list()):

                        # We are trying to convert each violation in the list to an ordered dictionary
                        # and put the ordered lists in order by violation id
                        if self.debug:
                            print('type is a list'+lineno())
                        new_violations = []
                        for violation in r['file_results']['violations']:

                            if type(violation) == type(list()):
                                if self.debug:
                                    print('violation is a list'+lineno())


                                temp_list = []

                                for items in violation:
                                    temp_list.append(items.to_hash())

                                new_violations.append(temp_list)

                            elif hasattr(violation, '__class__') and hasattr(violation.__class__,'__name__') and violation.__class__.__name__ == 'Violation':
                                 if self.debug:
                                     print('has class' + lineno())
                                     print('class: ' + str(violation.__class__.__name__) + lineno())

                                 new_violations.append(violation.to_hash())
                            else:

                                if self.debug:
                                    print('violation is not a list: '+lineno())

                                new_violations.append(violation.to_hash())

                        r['file_results'] = new_violations


                    elif type(r['file_results']['violations']) == type(dict()):
                        if self.debug:
                            print('is a dict'+lineno())
                        r['file_results'] = [violation.to_hash()]


                # If there are no violations in file results
                else:
                    if self.debug:
                        print('there are no violations: '+lineno())
                        print('type:'+str(type(r['file_results']))+lineno())
                    for item in r['file_results']:
                        if self.debug:
                            print('item: '+str(item)+lineno())
                            print('type: '+str(type(item))+lineno())
                        if hasattr(item,'__name__'):
                            if self.debug:
                                print('has name'+lineno())
                                print('name: '+str(item.__name__)+lineno())
                        if hasattr(item, '__class__') and hasattr(item.__class__,'__name__') and item.__class__.__name__ == 'Violation':
                            if self.debug:
                                print('has class' + lineno())
                                print('class: ' + str(item.__class__.__name__) + lineno())
                                print('dirs:'+str(dir(item))+lineno())


                                print('vars: '+str(vars(item))+lineno())

                            r['file_results'] = [item.to_hash()]


            hash = results

            order_of_keys = ["failure_count", "filename", "file_results"]


            if hash:
                if self.debug:
                    print("\n"+'## there is a hash: '+str(hash)+lineno())

                if type(hash) == type(list()):
                    if self.debug:
                        print('ist a list: '+str(lineno()))
                    # Iterate over each violation

                    if sys.version_info[0] < 3:
                        for item in sorted(hash):
                            if self.debug:
                                print("\n#################################")
                                print('item: '+str(item)+lineno())
                                print("#####################################\n")

                            my_ordered_dict= OrderedDict()
                            for key in order_of_keys:
                                my_ordered_dict[key] = item[key]

                            if self.debug:
                                print("\n"+'ordered dict is: '+str(my_ordered_dict)+lineno())

                            array_of_results.append(my_ordered_dict)

                            if self.debug:
                                print("\n"+'results: '+str(array_of_results)+lineno())
                    else:
                        for item in hash:
                            if self.debug:
                                print("\n#################################")
                                print('item: ' + str(item) + lineno())
                                print("#####################################\n")

                            my_ordered_dict = OrderedDict()
                            for key in order_of_keys:
                                my_ordered_dict[key] = item[key]

                            if self.debug:
                                print("\n" + 'ordered dict is: ' + str(my_ordered_dict) + lineno())

                            array_of_results.append(my_ordered_dict)

                            if self.debug:
                                print("\n" + 'results: ' + str(array_of_results) + lineno())

                # if not a list - FIXME
                else:
                    if self.debug:
                        print('is not a list: '+lineno())
                    for item in hash:
                        if self.debug:
                            print('item: '+str(item)+lineno())
                            print('hash item: '+str(hash[item])+lineno())

                        my_ordered_dict = OrderedDict()

                        for key in order_of_keys:
                            my_ordered_dict[key]= item[key]

                    if self.debug:
                        print('my ordered dict: '+str(my_ordered_dict)+lineno())


                    array_of_results.append(my_ordered_dict)


        # If the results is not a list, then assuming it is a hash...FIXME
        else:
            if self.debug:
                print('results is not a list: '+lineno())

            order_of_keys = ["failure_count", "filename", "file_results"]
            list_of_tuples = [(key, results[key]) for key in order_of_keys]
            new_results = OrderedDict(list_of_tuples)

            hash=[]
            for result in new_results:
                if self.debug:
                    print('result: '+str(result)+lineno())

                for item in result:

                    if item:
                        array_of_results.append(item.to_hash())

            if self.debug:
                print('returning: '+str(hash)+lineno())

        return self.pretty(array_of_results)