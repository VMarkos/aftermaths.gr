# config.py

import os


class Config:
    PWD = os.path.abspath(os.path.dirname(__file__))
    CONTENT_DIR = os.path.join(PWD, "..", "content")
    BACKUP_DIR = os.path.join(PWD, "__backup")
    CONTENT_ROOT = os.path.join(PWD, "__content")
    CONTENT_TREE = os.path.join(PWD, "content_tree.json")
