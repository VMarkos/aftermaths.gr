# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import re
import itertools as it
from datetime import datetime
from glob import glob
from dataclasses import asdict
from sphinx.application import Sphinx
from sphinxawesome_theme import ThemeOptions


def get_files_in_dir(directory: str, ext: str) -> [str]:
    return [y for x in os.walk(directory) for y in glob(os.path.join(x[0], f"*.{ext}"))]


def get_doc_date(path: str) -> datetime | None:
    with open(path, 'r') as file:
        for line in file.readlines():
            match = re.match(r'\s*:date: ([\d\-\:\s]+)', line)
            if match is not None:
                return datetime.strptime(match.group(1).strip(), '%Y-%m-%d %H:%M')
    return None


def generate_latest_entries(app: Sphinx) -> None:
    PWD = os.path.abspath(os.path.dirname(__file__))
    DOCS_DIR = os.path.join(PWD, 'docs')
    docs = get_files_in_dir(DOCS_DIR, 'rst')
    doc_dates = filter(lambda x: x[1] is not None and 'Πρόχειρα' not in x[0], zip(docs, map(get_doc_date, docs)))
    sorted_docs = map(lambda x: str(x[0]), sorted(doc_dates, key=lambda x: x[1]))
    five_latest = map(lambda x: x.split('sphinx/')[-1], it.islice(reversed(list(sorted_docs)), 5))
    fl_str = '\n\t'.join(five_latest)
    contents_str = ''
    with open('contents.rst', 'r') as file:
        add_line = True
        for line in file.readlines():
            if not add_line and 'toctree' in line:
                add_line = True
            if add_line:
                contents_str += line
            if 'Πρόσφατα' in line:
                contents_str += f'\n\t{fl_str}\n\n'
                add_line = False
    with open('contents.rst', 'w') as file:
        file.write(contents_str)


def setup(app: Sphinx):
    app.connect('builder-inited', generate_latest_entries)


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
html_css_files = ['custom.css']

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

