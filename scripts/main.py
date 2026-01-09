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
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def preprocess_filename(fname: str) -> str:
    return re.sub(r"-(?=[a-fA-F\d]{2})", r"%", fname)


def unencode_filename(fname: str) -> str:
    return unquote(fname)


def postprocess_filename(fname: str) -> str:
    return re.sub(r"\0", r"", fname)


def rename_rst_files(rst_files: [str]) -> None:
    logging.basicConfig(filename="main.log")
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
    fnames = get_files_in_dir(Config.CONTENT_DIR, "rst")
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
    _math_str = re.sub(r"\\displaystyle", r"", math_str)
    return clean_math_string(_math_str, " :math:`", "` ")


def fix_display_math(math_str: str) -> str:
    return clean_math_string(math_str, ".. math:: ", "")


def fix_content(
    path: str,
    fix_fn: Callable[[str, dict[str, any]], str],
    post_process: Callable[[str, dict[str, any]], None] | None = None,
    backup: bool = False,
) -> None:
    with open(path, "r") as file:
        old_lines = file.readlines()
    if backup:
        backup_file(path)
    fix_params = dict()
    with open(path, "w") as file:
        for line in old_lines:
            fixed_line = fix_fn(line, fix_params)
            file.write(fixed_line)
    if post_process:
        post_process(path, fix_params)


def math_fix_fn(line: str, params: dict[str, any] = dict()) -> str:
    if re.match(r"^\s*\$\s*latex\s+.+\$$", line):
        clean_line = fix_display_math(line)
    else:
        clean_line = fix_inline_math(line)
    return clean_line


def fix_math_content(path: str) -> None:
    fix_content(path, math_fix_fn)


def fwslash_fix_fn(line: str, params: dict[str, any] = dict()) -> str:
    clean_line = re.sub(r"\\\\", r"\\", line)
    clean_line = re.sub(r"\\displaystyle", r"", clean_line)
    return clean_line


def fix_forward_slashes(path: str) -> None:
    fix_content(path, fwslash_fix_fn)


def video_fix_fn(line: str, params: dict[str, any] = dict()) -> str:
    fixed_line = re.sub(
        r"https://www.youtube.com/watch\?v=(\w+)(?:&\w*)?", r".. youtube:: \1 ", line
    )
    return fixed_line


def fix_video_urls(path: str) -> None:
    fix_content(path, video_fix_fn)


def find_attachment_path(line) -> str | None:
    att_m = re.search(r"(?<=:attachments: ).+", line)
    return att_m.group(0) if att_m is not None else None


def find_image_caption(line) -> str | None:
    words = re.split(r"\s+", line)
    caption_prefix_ann = ("η", "κεντρική", "εικόνα", "είναι")
    caption_prefix_nan = ("η", "κεντρικη", "εικονα", "ειναι")
    caption_prefix = zip(caption_prefix_ann, caption_prefix_nan)
    is_valid_prefix = all(w.lower() in cp for (w, cp) in zip(words[:4], caption_prefix))
    if is_valid_prefix:
        return " ".join([words[4].capitalize()] + words[5:])
    return None


def main_image_fix_fn(line: str, params: dict[str, any] = dict()) -> str:
    att_path = find_attachment_path(line)
    if att_path:
        params["attachment"] = att_path
        return line
    image_caption = find_image_caption(line)
    if image_caption:
        params["caption"] = image_caption
        return '\n'
    return line


def build_rst_figure(attachment: str, caption: str) -> str:
    return (
        f"\n"
        f".. figure:: /{attachment}\n"
        f"\t:alt: {caption}\n"
        f"\t:align: center\n"
        f"\n"
        f"\t{caption}\n\n"
    )


def main_image_pp(path: str, params: dict[str, any]) -> None:
    with open(path, "r") as file:
        old_lines = file.readlines()
    if 'attachment' not in params.keys():
        logger.info(f'File {path} missing "attachment" key.')
        return
    if 'caption' not in params.keys():
        logger.info(f'File {path} missing "caption" key.')
        params["caption"] = ""
    rst_figure = build_rst_figure(**params)
    with open(path, "w") as file:
        for line in old_lines:
            file.write(line)
            if find_attachment_path(line):
                file.write("")
                file.write(rst_figure)


def fix_main_image(path: str) -> None:
    fix_content(path, main_image_fix_fn, main_image_pp)


def meta_fix_fn(line: str, params: dict[str, any]) -> str:
    in_meta = params.get('meta')
    match in_meta:
        case None:
            if re.match(r'^#+$', line.strip()):
                params['meta'] = True
                return "\n" + line.strip() + "\n\n.. meta::\n"
            else:
                return line.strip()
        case True:
            if re.match(r':attachments: ', line.strip()):
                params['meta'] = False
            return '\t' + line
        case False:
            return line



def fix_meta_content(path: str) -> None:
    fix_content(path, meta_fix_fn)


def create_content_tree(root: str) -> None:
    content_tree = { root: dict() }
    with open(Config.CONTENT_TREE, 'r') as file:
        content_tree[root] = json.load(file)
    visited = [] # BFS traversal of content_dir
    for d in category_dirs:
        Path(os.path.join(root, d)).mkdir(exist_ok=True)


def relocate_file(path: str) -> None:
    ...


def main():
    # rename_content()
    # restore_backups(Config.BACKUP_DIR, Config.CONTENT_DIR)
    # Fix content
    fnames = get_files_in_dir(Config.CONTENT_DIR, "rst")
    for file_path in tqdm(map(os.path.abspath, fnames)):
        # fix_math_content(file_path)
        # fix_forward_slashes(file_path)
        # fix_video_urls(file_path)
        # fix_main_image(file_path)
        # fix_meta_content(file_path)


if __name__ == "__main__":
    main()
