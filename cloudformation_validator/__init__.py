from __future__ import absolute_import, division, print_function
import pkg_resources
from cloudformation_validator.ValidateUtility import ValidateUtility #noqa

__version__ = pkg_resources.get_distribution('cloudformation_validator').version

__all__ = [
    'schema_registry',
    'rules_set_registry'
]
__title__ = 'cloudformation_validator'
__version__ = '0.6.19'
__author__ = 'Will Rubel'
__author_email__ = 'willrubel@gmail.com'

