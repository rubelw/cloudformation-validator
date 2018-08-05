from __future__ import absolute_import, division, print_function
import inspect
from cfn_model.transforms import Serverless


def lineno():
    """Returns the current line number in our program."""
    return str(' -  TransformRegistry- line number: '+str(inspect.currentframe().f_back.f_lineno))


class TransformRegistry:
    """
    Transform registry parser
    """
    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        #self.registry= {'AWS::Serverless-2016-10-31' = > CfnModel::Transforms::Serverless}
        self.registry = Serverless.Serverless(debug=debug)
        self.debug = debug

        if self.debug:
            print('TransformRegistry - init'+lineno())

    def perform_transforms(self,cfn_hash):
        if self.debug:
            print('TranformRegistry - perform_transforms'+lineno())

        if 'Transform' in cfn_hash:
            transform_name = cfn_hash['Transform']

            if transform_name:
                self.registry.perform_transform(cfn_hash)

        else:

            return cfn_hash

    def instance(self):
        if self.debug:
            print('TransformRegistry - instance'+lineno())
        #@instance| |= TransformRegistry.new
        #@instance
        # FIXME
        sys.exit(1)