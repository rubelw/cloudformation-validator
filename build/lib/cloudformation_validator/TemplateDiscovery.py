from __future__ import absolute_import, division, print_function
import os
import sys
import inspect

def lineno():
    """Returns the current line number in our program."""
    return str(' - TemplateDiscovery - line number: '+str(inspect.currentframe().f_back.f_lineno))


class TemplateDiscovery:
    """
    Template discover
    """

    def __init__(
            self, 
            input_json_path=str(os.path.dirname(__file__)+'/test_templates/json'),
            template_pattern='json', 
            debug=False
    ):
        """
        Initialize TemplateDiscovery
        :param input_json_path: 
        :param template_pattern: 
        :param debug: 
        """
        self.input_json_path = input_json_path
        self.template_pattern = template_pattern
        self.templates = []
        self.debug = debug

        if self.debug:
            print('TemplateDiscovery - __init__'+lineno())

    def discover_templates(self):
        """
        Discover templates
        :return: 
        """
        if self.debug:
            print("\n\n#######################################")
            print('discover templates'+lineno())
            print("###########################################\n\n")

            print('input_json_path: '+str(self.input_json_path)+lineno())
            print('template_pattern: '+str(self.template_pattern)+lineno())

            print(str(os.path.dirname(__file__)))
            print('cwd: '+str(os.chdir(os.path.dirname(__file__)))+lineno())

        template_filenames = []

        for root, directories, filenames in os.walk(self.input_json_path):
            for filename in filenames:
                if filename.endswith('.json') or filename.endswith('.yaml') or filename.endswith('.yml'):

                    if self.debug:
                        print(os.path.join(root, filename))

                    if 'AWSTemplateFormatVersion' in open(os.path.join(root,filename)).read():
                        template_filenames.append(os.path.join(root, filename))

        return template_filenames

    def render_path(self):
        """
        Render the path
        :return: 
        """
        if self.debug:
            print('render_path'+lineno())
        # FIXME
        sys.exit(1)
        return path
        # return path.path if path.is_a? File
        # path

    def find_templates_in_directory(self):
        """
        Find templates in directory
        :return: 
        """
        if self.debug:
            print('find_template_in_directory'+lineno())
        # FIXME
        sys.exit(1)
