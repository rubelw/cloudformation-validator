import inspect
import sys
from collections import OrderedDict


def lineno():
    """Returns the current line number in our program."""
    return str(' - RulesView - line number: '+str(inspect.currentframe().f_back.f_lineno))



class  RulesView:

    def emit(rule_registry, profile, debug=None):
        '''
        Emits something
        :param profile: 
        :return: 
        '''

        RulesView.emit_warnings(warnings=rule_registry.warnings(),profile=profile, debug=debug)
        RulesView.emit_failings(failings=rule_registry.failings(),profile=profile, debug=debug)


    def emit_warnings(warnings, profile, debug=None):
        '''
        Emits warnings
        :param profile: 
        :return: 
        '''
        if debug:
            print('emit_warnings '+lineno())
            print('warnings: '+str(warnings)+lineno())


        warnings_data={}
        #d_sorted_by_value = OrderedDict(sorted(d.items(), key=lambda x: x[1]))
        for rule in warnings:
            data = rule.to_hash()

            warnings_data[data['id']]=data

        keylist = list(warnings_data.keys())
        keylist.sort()

        print("##################################")
        print("########## WARNINGS ##############")
        print("##################################")

        for key in keylist:
            print("%s" % (warnings_data[key]))

        # FIXME FOR profile
        #do | warning |
        #if profile.nil?
        #puts
        #"#{warning.id} #{warning.message}"

        #elsif
        #profile.execute_rule?(warning.id)
        #puts
        #"#{warning.id} #{warning.message}"


    def emit_failings(failings, profile, debug=None):
        '''
        Emits failings
        :param profile: 
        :return: 
        '''

        if debug:
            print('emit_failings ' + lineno())


        failings_data={}
        for rule in failings:
            data = rule.to_hash()

            failings_data[data['id']]=data

        keylist = list(failings_data.keys())
        keylist.sort()

        print("##################################")
        print("########## FAILINGS #############")
        print("##################################")

        for key in keylist:
            print("%s" % (failings_data[key]))


        #elsif
        #profile.execute_rule?(failing.id)
        #puts
        #"#{failing.id} #{failing.message}"


