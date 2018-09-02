from __future__ import absolute_import, division, print_function
import sys

class Parameter:
    """
    Parameter model
    """
    def __init__(self, debug=False):
        """
        Initialize
        :param debug:
        """
        #   attr_accessor :id, :type
        # attr_accessor :synthesized_value
        self.id = None
        self.type = None
        self.instance_variables = []
        self.debug= debug

        if self.debug:
            print('Parameter - init')

    def is_no_echo(self):
        """
        ???
        :return:
        """
        if self.debug:
            print('is_no_echo')
        # FIXME
        sys.exit(1)
        #!@noEcho.nil? && @noEcho.to_s.downcase == 'true'


    def to_string(self):
        """
        ???
        :return:
        """
        if self.debug:
            print('to_s')
        # FIXME
        sys.exit(1)
        #    << END
        #{
        #    # {emit_instance_vars}
        #}

    def method_missing(self, method_name, *args):
        """
        ???
        :param method_name:
        :param args:
        :return:
        """
        if self.debug:
            print('method_missing')
        # FIXME
        sys.exit(1)
        #if method_name =~ /^(\w+)=$/
        #  instance_variable_set "@#{$1}", args[0]
        #else
        #  instance_variable_get "@#{method_name}"


    def emit_instance_vars(self):
        """
        ???
        :return:
        """
        if self.debug:
            print('emit_instance_varts')

        # FIXME
        sys.exit(1)
        #instance_vars_str = ''
        #self.instance_variables.each do |instance_variable|
        #  instance_vars_str += "  #{instance_variable}=#{instance_variable_get(instance_variable)}\n"
        #end
        #instance_vars_str