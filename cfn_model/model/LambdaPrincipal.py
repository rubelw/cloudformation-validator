
class LambdaPrincipal:

    @staticmethod
    def wildcard(context):
        '''
        If contains wildcard
        :return: 
        '''
        if type(context) == type(str()):
            if '*' in context:
                return True

        return False
