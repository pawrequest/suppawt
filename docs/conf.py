# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from datetime import datetime
from importlib.metadata import version as metadata_version  # dont clash with version in sphinx

project = 'PawSupport'
# copyright = '2024, PawRequest'
author = 'PawRequest'
release = '0.0.1'

copyright = f'2024, {author}'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx_readme',
    # 'sphinx.ext.napoleon',
    # 'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_context = {
    'display_github': True,
    'github_user': 'PawRequest',
    'github_repo': 'pawsupport',
}

html_baseurl = "https://pawsupport.readthedocs.io/en/latest"

readme_src_files = "index.rst"

readme_docs_url_type = "code"
