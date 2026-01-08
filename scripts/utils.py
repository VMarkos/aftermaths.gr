# utils.py

import os
from glob import glob
import shutil as sh
import functools as ft
from config import Config


def compose_2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return ft.reduce(compose_2, fs)


def backup_file(path: str) -> None:
    if not os.path.exists(Config.BACKUP_DIR):
        os.mkdir(Config.BACKUP_DIR)
    bname = os.path.basename(path)
    sh.copyfile(path, os.path.join(Config.BACKUP_DIR, bname + ".bak"))


def restore_backups(backup_dir: str, target_dir: str) -> None:
    # Assume both directories exist
    bfiles = get_files_in_dir(Config.BACKUP_DIR, "bak")
    for file in map(os.path.abspath, bfiles):
        clean_name = os.path.splitext(os.path.abspath(file))[0]
        sh.copyfile(file, clean_name)


def get_files_in_dir(directory: str, ext: str) -> [str]:
    return [y for x in os.walk(directory) for y in glob(os.path.join(x[0], f"*.{ext}"))]
