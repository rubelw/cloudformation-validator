import inspect
from cfn_model.model.Principal import Principal


def lineno():
    """Returns the current line number in our program."""
    return str(' - Statement - line number: '+str(inspect.currentframe().f_back.f_lineno))


class Statement:

    def __init__(self, debug=False):
        '''
        Initialize
        :param debug: 
        '''
        self.debug=debug

        if self.debug:
            print("\n\n#############################")
            print('Statement __init__'+lineno())
            print('debug: '+str(debug)+lineno())
            print("################################\n")

        self.actions=[]
        self.not_actions = []
        self.resources = []
        self.not_resources = []
        self.sid = None
        self.effect = None
        self.condition = None
        self.principal = None
        self.not_principal = None

        if self.debug:
            print('init')

    def wildcard_actions(self):
        '''
        wildcard actions
        :return: 
        '''
        if self.debug:
            print('wildcard_actions'+lineno())

        actions= []

        for action in self.actions:
            if self.debug:
                print('action: '+str(action)+lineno())
                print('type: '+str(type(action))+lineno())

            if type(action)== type(str()) or type(action) == type(unicode()):
                if '*' in action:
                    actions.append(action)

            elif type(action)==type(list()):
                for item in action:

                    if '*' in item:
                        actions.append(item)
                    else:
                        if self.debug:
                            print("No match!!"+lineno())

        return actions

    def wildcard_principal(self):
        '''
        Get wildcard principals
        :return: 
        '''
        if self.debug:
            print('wildcard_principal'+lineno())

        principal = Principal(debug=self.debug)
        return principal.wildcard(self.principal)

    def wildcard_resources(self):
        '''
        Get wildcard resources
        :return: 
        '''
        if self.debug:
            print('wildcard_resources'+lineno())

        resources = []

        for resource in self.resources:
            if self.debug:
                print('resource: '+str(resource)+lineno())

            if type(resource)== type(str()) or type(resources) == type(unicode()):
                if '*' in resource:
                    resources.append(resource)

            if type(resource)== type(dict()):
                if self.debug:
                    print('is a dict'+lineno())
                for item in resource:
                    if self.debug:
                        print('item: '+str(item)+lineno())
                        print('resource item: '+str(resource[item])+lineno())

                    if type(resource[item]) == type(list()):
                        for more_items in resource[item]:
                            if self.debug:
                                print('more items: '+str(more_items)+lineno())

                            if type(more_items) == type(str()) or type(more_items) == type(unicode()):
                                if '*' in more_items:
                                    resources.append(more_items)

                            elif type(more_items) == type(list()):
                                if self.debug:
                                    print('is a list'+lineno())
                                for many_more_items in more_items:
                                    if self.debug:
                                        print('many more items: '+str(many_more_items)+lineno())

                                    if type(many_more_items)== type(str()) or type(many_more_items) == type(unicode()):
                                        if '*' in many_more_items:
                                            resources.append(many_more_items)

            if type(resource) == type(list()):
                for item in resource:

                    if '*' in item:
                        resources.append(item)
                    else:
                        if self.debug:
                            print("No match!!"+lineno())

        return resources