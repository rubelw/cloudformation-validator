from __future__ import absolute_import, division, print_function
import inspect
import sys


def lineno():
    """Returns the current line number in our program."""
    return str(' - ModelElement - line number: '+str(inspect.currentframe().f_back.f_lineno))


class ModelElement():
    """
    Model element
    """
    def __init__(self, cfn_model, debug=False):
        """
        Initialize
        :param cfn_model:
        :param debug:
        """
        # attr_accessor :logical_resource_id, :resource_type, :metadata
        self.logical_resource_id = None
        self.resource_type = None
        self.metadata = None
        self.debug= debug

        self.cfn_model = cfn_model
        if self.debug:
            print('ModelElement - init'+lineno())

    def another_element(self, another_model_element):
        """
        ???
        :param another_model_element:
        :return:
        """
        if self.debug:
            print('another element'+lineno())
        # FIXME
        sys.exit(1)
        #found_unequal_instance_var = false
        #instance_variables_without_at_sign.each do |instance_variable|
        #  if instance_variable != :logical_resource_id && instance_variable != :cfn_model
        #    if self.send(instance_variable) != another_model_element.send(instance_variable)
        #      found_unequal_instance_var = true
        #    end
        #  end
        #end
        #!found_unequal_instance_var

    def method_missing(self, method_name, *args):
        """
        ???
        :param method_name:
        :param args:
        :return:
        """
        if self.debug:
            print('method_missing'+lineno())
        # FIXME
        sys.exit(1)
        #if method_name =~ / ^ (\w+)=$ /
        #instance_variable_set
        #"@#{$1}", args[0]

        #else
        #References.resolve_value( @ cfn_model, instance_variable_get("@#{method_name}"))
        #end

    def instance_variables_without_at_sign(self):
        """
        Instance variables without an at sign
        :return:
        """
        if self.debug:
            print('instance_variables_without_at_sign'+lineno())
        # FIXME
        sys(exit)
        #self.instance_variables.map { |instance_variable| strip(instance_variable) }

    def strip(self, sym):
        """
        ???
        :param sym:
        :return:
        """
        if self.debug:
            print('strip'+lineno())

        # FIXME
        sys.exit(1)
        #sym.to_s.gsub( / @ /, '').to_sym

    def emit_instance_vars(self):
        """
        ???
        :return:
        """
        if self.debug:
            print('emit_instance_vars'+lineno())

        instance_vars_str = ''

        sys.exit(1)
        #for variable in self.instance_variables_without_at_sign()
        #self.instance_variables.each do |instance_variable|
        #  instance_vars_str += "  #{instance_variable}=#{instance_variable_get(instance_variable)}\n"

        #return instance_vars_str