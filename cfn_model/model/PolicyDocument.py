from __future__ import absolute_import, division, print_function
import inspect
import sys
from builtins import (str)


def lineno():
    """Returns the current line number in our program."""
    return str(' - PolicyDocument - line number: '+str(inspect.currentframe().f_back.f_lineno))


class PolicyDocument:
    """
    Policy document model
    """

    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        self.statements = []
        self.version = None
        self.debug = debug

        if self.debug:
            print('init'+lineno())

    def wildcard_allowed_resources(self, debug=False):
        """
        Whether allow wildcard resources
        :param debug: 
        :return: 
        """
        if self.debug or debug:
            print('wilcard_allowed_resources'+lineno())

        for statement in self.statements:

            if len(statement.wildcard_resources())>0 and str(statement.effect) == 'Allow':
                return True

        return False


    def wildcard_allowed_actions(self, debug=False):
        """
        Wether wildcard allowed actions
        :param debug: 
        :return: 
        """
        if self.debug or debug:
            print('wildcard_allowed_actions'+lineno())

        for statement in self.statements:
            if self.debug or debug:

                print("\n\n#######################################################")
                print('statement in policy document: '+str(statement)+lineno())
                print('vars: '+str(vars(statement)))
                print('wildcard_actions:'+str(statement.wildcard_actions()))
                print("#######################################################\n")

            if str(statement.effect) == 'Allow':
                if self.debug or debug:
                    print('effect is to allow'+lineno())

                for action in statement.actions:
                    if self.debug or debug:
                        print('action: '+str(action)+lineno())
                        print('action type: '+str(type(action))+lineno())

                    if type(action) == type(str()):
                        if '*' in action:
                            return True

                    if sys.version_info[0] < 3 and type(action) == type(unicode()):
                            if '*' in str(action):
                                return True

                    elif type(action)== type(list()):
                        for action2 in action:
                            if self.debug or debug:
                                print('action: '+str(action2)+lineno())

                            if "*" in action2:
                                if self.debug or debug:
                                    print('* in action')
                                return True

        return False



    def wildcard_allowed_principals(self, debug=False):
        """
        Whether wildcard allowed principals
        :param debug: 
        :return: 
        """
        if self.debug or debug:
            print('wildcard_allowed_principals'+lineno())
            print('self: '+str(self)+lineno())
            print('vars: '+str(vars(self))+lineno())
            print('number of statements: '+str(len(self.statements))+lineno())

        for statement in self.statements:
            if self.debug or debug:
                print('statment: '+str(statement)+lineno())
                print('vars: '+str(vars(statement)))
                print('wildcard_principal:'+str(statement.wildcard_principal())+lineno())

            if str(statement.effect) == 'Allow':
                if self.debug or debug:
                    print('effect is to allow'+lineno())

                if statement.wildcard_principal():
                    return True

        return False


    def allows_not_action(self, debug=False):
        """
        Select any statement object that allow in conjunction with a NotAction
        :param debug: 
        :return: 
        """
        if self.debug or debug:
            print('allows_not_action'+lineno())

        for statement in self.statements:
            if self.debug or debug:
                print('statement: '+str(statement)+lineno())
                print('vars: '+str(vars(statement))+lineno())

            if len(statement.not_actions) > 0 and str(statement.effect) == 'Allow':
                if self.debug or debug:
                    print('has not actions and effect is allow'+lineno())
                return True

        return False



    def allows_not_resource(self, debug=False):
        """
        Allows not resource
        :param debug: 
        :return: 
        """
        if self.debug or debug:
            print('allows_not_resources'+lineno())

        for statement in self.statements:
            if self.debug or debug:
                print('statement: '+str(statement)+lineno())

            if type(statement)== type(dict()):

                if 'NotResource' in statement and 'Effect' in statement:
                    if len(statement['NotResource'])>0 and statement['Effect'] == 'Allow':
                        return True

            elif hasattr(statement,'not_resources') and hasattr(statement,'effect'):

                    if len(statement.not_resources)>0 and str(statement.effect) == 'Allow':
                        return True

        return False

    def allows_not_principal(self, debug=False):
      """
      Allows not principal
      :param debug: 
      :return: 
      """
      if self.debug or debug:
        print('allows_not_principal'+lineno())

      for statement in self.statements:
          if self.debug or debug:
              print('statement: ' + str(statement) + lineno())

          if type(statement) == type(dict()):

              if 'NotPrincipal' in statement and 'Effect' in statement:
                  if len(statement['NotPrincipal']) > 0 and statement['Effect'] == 'Allow':
                      return True

          elif hasattr(statement, 'not_principal') and hasattr(statement, 'effect'):
              if statement.not_principal and statement.effect:
                  if len(statement.not_principal) > 0 and str(statement.effect) == 'Allow':
                    return True

      return False


    def to_string(self):
        """
        Convert to string
        :return: 
        """
        if self.debug:
            print('to_s'+lineno())
        # FIXME
        sys.exit(1)
        #<< END

        #{
        #    version =  # {@version}
        #statements =
        # {@statements}
        #}