# config.py

import os


class Config:
    PWD = os.path.abspath(os.path.dirname(__file__))
    CONTENT_DIR = os.path.join(PWD, "..", "content")
    CONTENT_STRUCT_DIR = os.path.join(PWD, "__content")
    BACKUP_DIR = os.path.join(PWD, "__backup")
    CONTENT_ROOT = os.path.join(PWD, "__content")
    CONTENT_TREE = os.path.join(PWD, "content_tree.json")
    TAGMAP = os.path.join(PWD, "tagmap.json")
    SPHINX_WD = os.path.join(PWD, '..', '..', 'sphinx')
    SPHINX_DOCS = os.path.join(SPHINX_WD, 'docs')
