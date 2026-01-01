# utils.py

import os


def ensure_path_exists(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path)
    return path
