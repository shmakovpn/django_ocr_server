"""
doc/source/conf.py
++++++++++++++++++

Sphinx configuration file of django_ocr_server

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2021-01-19
"""
from typing import List
import os
import sys

# -- Project information -----------------------------------------------------

project: str = 'django_ocr_server'
copyright: str = '2019, shmakovpn'
author: str = 'shmakovpn'

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR: str = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR: str = os.path.dirname(DOCS_DIR)
PACKAGE_DIR: str = os.path.join(PROJECT_DIR, project)
sys.path.insert(0, PROJECT_DIR)  # need to import django_ocr_server
sys.path.insert(
    0, SCRIPT_DIR
)  # need to find doc/source/requirements.txt instead of project requirements.txt

# mocking C modules
# autodock_mock_imports: List[str] = []

VERSION: str = ''
with open(os.path.join(PACKAGE_DIR, 'version.py')) as version_file:
    exec(version_file.read())

# The short X.Y version
version: str = VERSION
# The full version, including alpha/beta/rc tags
release: str = VERSION

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: List[str] = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

master_doc: str = 'contents'

# Add any paths that contain templates here, relative to this directory.
templates_path: List[str] = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme: str = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: List[str] = ['_static']
