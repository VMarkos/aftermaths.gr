# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from dataclasses import asdict
from sphinxawesome_theme import ThemeOptions

project = 'aftermaths'
copyright = '2026, aftermaths'
author = 'aftermaths'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.youtube',
    'sphinx_favicon',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv/*']

language = 'el'

master_doc = "contents"

highlight_language = 'python3'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = 'aftermaths'
html_permalinks_icon = '<span>#</span>'
html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']

favicons = [
    'icons/favicon.ico',
]

html_sidebars = {
    '**': ['sidebar_main_nav_links.html', 'sidebar_toc.html']
}

theme_options = ThemeOptions(
    show_breadcrumbs = True,
    main_nav_links = {
        "Σχετικά": "/about",
        "Πανελλήνιες": "/panellinies",
        "Υλικό": "docs/διδακτικό-υλικό",
        # "Εργαλεία": "/tools",
        "Επικοινωνία": "/contact",
    },
    awesome_external_links = True,
)

html_theme_options = asdict(theme_options)

html_theme_options['navigation_depth'] = 4
html_theme_options['show_nav_level'] = 4
