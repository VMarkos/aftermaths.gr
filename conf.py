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

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'el'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = 'aftermaths'
html_permalinks_icon = '<span>#</span>'
html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']

html_sidebars = {
    '**': ['sidebar_main_nav_links.html', 'sidebar_toc.html']
}

theme_options = ThemeOptions(
    show_breadcrumbs = True,
    main_nav_links = {
        "Σχετικά": "/about",
        "Πανελλήνιες": "/panellinies",
        "Υλικό": "/materials",
        "Εργαλεία": "/tools",
        "Επικοινωνία": "/contact",
    },
)

html_theme_options = asdict(theme_options)
