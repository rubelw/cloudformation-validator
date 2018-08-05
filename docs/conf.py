# -*- coding: utf-8 -*-
# cloudformation_validator documentation build configuration file
import cloudformation_validator


# -- General configuration ------------------------------------------------

# Minimal Sphinx version
needs_sphinx = '1.4'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Suffix(es) of source filenames. Ex: source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

# Master toctree document
master_doc = 'index'

# General project information
project = u'cloudformation_validator'
copyright = u'2018, δ'
author = u'δ'
language = 'en'
version = cloudformation_validator.__version__
release = cloudformation_validator.__version__

# List of file/dir patterns to ignore, relative to source directory
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Extension configuration ----------------------------------------------

# Extension modules
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

# Suppress warnings from add_documenter in config_spec_documenter
suppress_warnings = ['app.add_directive']

# Linkable external Sphinx docs
intersphinx_mapping = {
    'celery': ('http://docs.celeryproject.org/en/latest/', None),
    'python2': ('https://docs.python.org/2', None),
    'python3': ('https://docs.python.org/3', None),
    'sqlalchemy': ('http://docs.sqlalchemy.org/en/latest/', None),
    'boto3': ('http://boto3.readthedocs.io/en/latest/', None),
    'botocore': ('http://botocore.readthedocs.io/en/latest/', None),
    'sphinx': ('http://code.nabla.net/doc/sphinx/', None),
}

# External link shorteners (for refs that intersphinx can't handle)
extlinks = {
    'aws': ('http://docs.aws.amazon.com/%s', None),
    'boto3': ('http://boto3.readthedocs.io/en/latest/reference/%s', None),
    'celery': ('http://celery.readthedocs.org/en/latest/%s', None),
    'haskell': ('http://hackage.haskell.org/package/base-4.9.0.0/docs/%s', None),
    'jira': ('https://jira.phibred.com/browse/%s', ''),
    'python2': ('https://docs.python.org/2/library/%s', None),
    'python3': ('https://docs.python.org/3/library/%s', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable/%s', None),
    'sqlalchemy': ('http://docs.sqlalchemy.org/en/latest/%s', None),
    'wiki': ('https://gitlab.encirca.auto.pioneer.com/public-projects/developer-guide/wikis/%s', None),
    'six': ('https://pythonhosted.org/six/#%s', None)
}

# Google/Numpydoc settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False

# (Currently unused) link resolver for sphinx.ext.linkcode, to link to GitLab source code
# gitlab_repo = 'https://gitlab.encirca.auto.pioneer.com/ccmmo/alina/blob/master'
# def linkcode_resolve(domain, info):
#     print('Domain: {} | Info: {}'.format(domain, info))
#     if domain != 'py' or not info['module']:
#         return None
#     filename = info['module'].replace('.', '/')
#     return '{}/{}.py'.format(gitlab_repo, filename)


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages. Builtin themes:
# http://www.sphinx-doc.org/en/latest/theming.html
html_theme = 'nature'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Cloudformation-Validator'

# Image to place at the top of the sidebar
# html_logo = 'alina.jpg'

# Favicon image (.ico format, 16x16 or 32x32)
# html_favicon = 'tagger.ico'


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
# man_pages = [(master_doc, 'alina', 'Alina', [author], 1)]

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
