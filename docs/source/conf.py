# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from nifi_deploy import __version__


# -- Project information -----------------------------------------------------

project = 'nifi-deploy'
copyright = '2018, Mads H. Jakobsen'
author = 'Mads H. Jakobsen'

# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# needs_sphinx = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

language = None

exclude_patterns = []

pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# html_theme_options = {}

html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'], }


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = 'nifi-deploydoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
}

latex_documents = [
    (master_doc, 'nifi-deploy.tex', 'nifi-deploy Documentation',
     'Mads H. Jakobsen', 'manual'),
]


# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, 'nifi-deploy', 'nifi-deploy Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (master_doc, 'nifi-deploy', 'nifi-deploy Documentation',
     author, 'nifi-deploy', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------