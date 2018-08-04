from __future__ import absolute_import, division, print_function
import sys
import inspect
from cloudformation_validator.Violation import Violation


def lineno():
    """Returns the current line number in our program."""
    return str(' - BaseRule - caller: '+str(inspect.stack()[1][3])+' - line number: '+str(inspect.currentframe().f_back.f_lineno))


# Base class all Rules should subclass
class BaseRule():
    """
    Base rule
    """

    def __init__(self, cfn_model=None, debug=False):
        """
        Initialize BaseRule
        :param cfn_model:
        :param debug:
        """
        self.cfn_model = cfn_model
        self.type = None
        self.id = None
        self.debug = debug

    
    def audit_impl(self):
        """
        Returns a collection of logical resource ids
        :return:
        """
        raise 'must implement in subclass'
    
    
    def audit(self):
        """
        Returns nil when there are no violations
        Returns a Violation object otherwise
        :return:
        """
        if self.debug:
            print("\n\n##########################################")
            print('BaseRule - audit'+lineno())
            print('calling audit_impl on rule')
            print("##############################################\n")
        
        logical_resource_ids =  self.audit_impl()
        
        if logical_resource_ids:
            if self.debug:
                print('logical ids: '+str(logical_resource_ids)+lineno())
        
            violation = Violation(id=self.rule_id(), type= self.rule_type(), message= self.rule_text(), logical_resource_ids= logical_resource_ids, debug=self.debug)
        
            if self.debug:
                print('violation: '+str(vars(violation))+lineno())
        
            return violation
        
        else:
            if self.debug:
                print('no logical ids: '+lineno())
            return