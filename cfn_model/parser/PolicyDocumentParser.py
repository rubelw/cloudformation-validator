from __future__ import absolute_import, division, print_function
import sys
import inspect
from cfn_model.model.PolicyDocument import PolicyDocument
from cfn_model.model.Statement import Statement


def lineno():
    """Returns the current line number in our program."""
    return str(' - PolicyDocumentParser - line number: '+str(inspect.currentframe().f_back.f_lineno))


class PolicyDocumentParser:
    """
    Policy document parser
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        self.debug = debug

        if self.debug:
            print('ParserError - init'+lineno())

    def parse(self, raw_policy_document):

        if self.debug:
            print("\n\n################################")
            print('PolicyDocumentParser - parse'+lineno())
            print("####################################\n\n")

            print('raw_policy_document: '+str(raw_policy_document)+lineno())

        policy_document = PolicyDocument(debug=self.debug)

        if 'Version' in raw_policy_document:

            policy_document.version = raw_policy_document['Version']

        if 'Statement' in raw_policy_document:
            if self.debug:
                print('has statement in raw policy document'+lineno())
                print('statement: '+str(raw_policy_document['Statement']))

            if type(raw_policy_document['Statement'])==type(list()):

                if len(raw_policy_document['Statement'])>1:
                    if self.debug:
                        print('more than one statemnt')

                for statement in raw_policy_document['Statement']:
                    if self.debug:
                        print('statement: '+str(statement)+lineno())
                    streamlined_array = self.streamline_array(statement)
                    parsed_statement = self.parse_statement(streamlined_array)
                    if self.debug:
                        print('parsed_statement: '+str(parsed_statement)+lineno())
                    policy_document.statements.append(parsed_statement)

            elif type(raw_policy_document['Statement'])== type(dict()):

                if self.debug:
                    print('statement: ' + str(raw_policy_document['Statement'])+lineno())

                parsed_statement = self.parse_statement(raw_policy_document['Statement'])
                if self.debug:
                    print('parsed_statement: ' + str(parsed_statement) + lineno())
                policy_document.statements.append(parsed_statement)


            elif type(raw_policy_document['Statement']) == type(str()):
                if self.debug:
                    print('statement: ' + str(raw_policy_document['Statement'])+lineno())

                parsed_statement = self.parse_statement(raw_policy_document['Statement'])
                if self.debug:
                    print('parsed_statement: ' + str(parsed_statement) + lineno())
                policy_document.statements.append(parsed_statement)


            else:
                if self.debug:
                    print('unknown type: '+lineno())
                sys.exit(1)

            if self.debug:
                print('policy_document: '+str(vars(policy_document))+lineno())
                print('statments'+str(policy_document.statements)+lineno())
                print('statement types: '+str(type(policy_document.statements))+lineno())
                print('type: '+str(type(policy_document))+lineno())

        return policy_document



    def parse_statement(self, raw_statement):
        """
        Parse statement
        :param vraw_statement: 
        :return: 
        """
        if self.debug:
            print('parse_statement'+lineno())
            print('raw_statement: '+str(raw_statement)+lineno())
            print('raw statement type is: '+str(type(raw_statement))+lineno())


        statement = Statement(self.debug)
        if 'Effect' in raw_statement:
            statement.effect = raw_statement['Effect']
        if 'Sid' in raw_statement:
            statement.sid = raw_statement['Sid']
        if 'Condition' in raw_statement:
            statement.condition = raw_statement['Condition']
        if 'Action' in raw_statement:
            statement.actions.append(raw_statement['Action'])
        if 'NotAction' in raw_statement:
            statement.not_actions.append(raw_statement['NotAction'])
        if 'Resource' in raw_statement:
            statement.resources.append(raw_statement['Resource'])
        if 'NotResource' in raw_statement:
            statement.not_resources.append(raw_statement['NotResource'])
        if 'Principal' in raw_statement:
            statement.principal = raw_statement['Principal']
        if 'NotPrincipal' in raw_statement:
            statement.not_principal = raw_statement['NotPrincipal']

        if self.debug:
            print('raw_statement: '+str(raw_statement)+lineno())
            if statement.condition:
                print('condition: '+str(statement.condition)+lineno())
            if statement.actions:
                print('actions: '+str(statement.actions)+lineno())
            if statement.sid:
                print('sid: '+str(statement.sid)+lineno())
            if statement.effect:
                print('effect: '+str(statement.effect)+lineno())
            if statement.resources:
                print('resources: '+str(statement.resources)+lineno())
            if statement.principal:
                print('principal: '+str(statement.principal)+lineno())
            if statement.not_principal:
                print('not_principal: '+str(statement.not_principal)+lineno())

            print("\n\n###############################################")
            print("statement: "+str(vars(statement))+lineno())
            print(' wildcard_actions:'+str(statement. wildcard_actions())+lineno())
            print('wildcard_principal: '+str(statement.wildcard_principal())+lineno())
            print('wildcard_resources: '+str(statement.wildcard_resources())+lineno())
            print("#####################################################\n")

        return statement

    def streamline_array(self, one_or_more):
        """
        ???
        :param one_or_more: 
        :return: 
        """

        if one_or_more:
            if self.debug:
                print('one_or_more: '+str(one_or_more)+lineno())


            if type(one_or_more) == type(str()):
                if self.debug:
                    print('is a string '+lineno())
                return one_or_more
            elif type(one_or_more)==type(dict()):
                if self.debug:
                    print('is a dict: '+lineno())


                return one_or_more
            elif type(one_or_more)==type(list()):
                if self.debug:
                    print('is an array: '+lineno())
                return one_or_more

            else:
                raise "unexpected object in streamline_array "+str(one_or_more)
        # FIXME
        sys.exit(1)
        return None


