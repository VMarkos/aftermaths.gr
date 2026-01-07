# main.py

import os
import re
import logging
from pathlib import Path
from glob import glob
from tqdm import tqdm
from urllib.parse import unquote
from config import Config
from utils import compose, backup_file, get_files_in_dir, restore_backups
from typing import Callable

logger = logging.getLogger(__name__)


def preprocess_filename(fname: str) -> str:
    return re.sub(r"-(?=[a-fA-F\d]{2})", r"%", fname)


def unencode_filename(fname: str) -> str:
    return unquote(fname)


def postprocess_filename(fname: str) -> str:
    return re.sub(r"\0", r"", fname)


def rename_rst_files(rst_files: [str]) -> None:
    logging.basicConfig(filename="main.log", level=logging.ERROR)
    logger.info("Starting...")
    err_count = 0
    process = compose(postprocess_filename, unencode_filename, preprocess_filename)
    for new_file, old_file in zip(map(process, rst_files), rst_files):
        try:
            os.rename(old_file, new_file)
        except Exception as e:
            logger.error(e)
            err_count += 1
    logger.info(f"Ended with {err_count} errors." "For more: {__name__}.log.")


def rename_content():
    fnames = get_files_in_dir(Config.CONTENT_DIR, 'rst')
    rename_rst_files(fnames)


def clean_math_string(math_str: str, math_left: str, math_right: str) -> str:
    hex_color = r"[a-fA-F\d]{0,6}"
    math_color = re.compile(r"&bg={}&fg={}".format(hex_color, hex_color))
    _math_str = re.sub(math_color, r"", math_str)
    str_start = re.compile(r"\$\s*latex\s+")
    str_end = re.compile(r"\s*\$")
    str_content = re.compile(r"([^\$]+)")
    pattern = re.compile(str_start.pattern + str_content.pattern + str_end.pattern)
    repl = r"{}\1{}".format(math_left, math_right)
    return re.sub(pattern, repl, _math_str)

def fix_inline_math(math_str: str) -> str:
    _math_str = re.sub(r'\\displaystyle', r'', math_str)
    return clean_math_string(_math_str, ' :math:`', '` ')


def fix_display_math(math_str: str) -> str:
    return clean_math_string(math_str, '.. math:: ', '')


def fix_content(path: str, fix_fn: Callable[[str], str], backup: bool=False) -> None:
    with open(path, 'r') as file:
        old_lines = file.readlines()
    if backup:
        backup_file(path)
    with open(path, 'w') as file:
        for line in old_lines:
            fixed_line = fix_fn(line)
            file.write(fixed_line)


def math_fix_fn(line: str) -> str:
    if re.match(r"^\s*\$\s*latex\s+.+\$$", line):
        clean_line = fix_display_math(line)
    else:
        clean_line = fix_inline_math(line)
    return clean_line

def fix_math_content(path: str) -> None:
    fix_content(path, math_fix_fn)


def fwslash_fix_fn(line: str) -> str:
    clean_line = re.sub(r'\\\\', r'\\', line)
    clean_line = re.sub(r'\\displaystyle', r'', clean_line)
    return clean_line

def fix_forward_slashes(path: str) -> None:
    fix_content(path, fwslash_fix_fn)


def video_fix_fn(line: str) -> str:
    fixed_line = re.sub(r'https://www.youtube.com/watch\?v=(\w+)(?:&\w*)?', r'.. youtube:: \1 ', line)
    return fixed_line


def fix_video_urls(path: str) -> None:
    fix_content(path, video_fix_fn)


def main():
    # rename_content()
    # restore_backups(Config.BACKUP_DIR, Config.CONTENT_DIR)
    # Fix content
    fnames = get_files_in_dir(Config.CONTENT_DIR, 'rst')
    for file_path in tqdm(map(os.path.abspath, fnames)):
        # fix_math_content(file_path)
        # fix_forward_slashes(file_path)
        fix_video_urls(file_path)


if __name__ == "__main__":
    main()
