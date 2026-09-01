# main.py

import os
import re
import json
import logging
import shutil as sh
from pathlib import Path
from glob import glob
from tqdm import tqdm
from urllib.parse import unquote
from config import Config
from utils import compose, backup_file, get_files_in_dir, restore_backups
from PostMap import PostMap
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
    fix_fn: Callable[[str, dict[str, object]], str],
    post_process: Callable[[str, dict[str, object]], None] | None = None,
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


def math_fix_fn(line: str, params: dict[str, object] = dict()) -> str:
    if re.match(r"^\s*\$\s*latex\s+.+\$$", line):
        clean_line = fix_display_math(line)
    else:
        clean_line = fix_inline_math(line)
    return clean_line


def fix_math_content(path: str) -> None:
    fix_content(path, math_fix_fn)


def fwslash_fix_fn(line: str, params: dict[str, object] = dict()) -> str:
    clean_line = re.sub(r"\\\\", r"\\", line)
    clean_line = re.sub(r"\\displaystyle", r"", clean_line)
    return clean_line


def fix_forward_slashes(path: str) -> None:
    fix_content(path, fwslash_fix_fn)


def video_fix_fn(line: str, params: dict[str, object] = dict()) -> str:
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


def main_image_fix_fn(line: str, params: dict[str, object] = dict()) -> str:
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


def main_image_pp(path: str, params: dict[str, object]) -> None:
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


def meta_fix_fn(line: str, params: dict[str, object]) -> str | None:
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
    def __mkdir(d: str) -> None:
        if not os.path.isdir(d):
            os.mkdir(d)
    def rec_mkdir(dir_json: dict[str, dict | None]) -> None:
        for d in dir_json.keys():
            __mkdir(d)
            if dir_json[d] is not None:
                os.chdir(d)
                rec_mkdir(dir_json[d])
                os.chdir('..')
    # Start recursion
    rec_mkdir(content_tree)


def relocate_file(path: str) -> None:
    fname = os.path.basename(path)
    pm = PostMap(path)
    pm_path = pm.get_target_path()
    target_path = os.path.join(pm_path, fname)
    sh.copyfile(path, target_path)


def fix_raw_html_videos(path: str) -> None:
    fix_content(path, raw_fix_fn)


def raw_fix_fn(line: str, params: dict[str, any]=dict()) -> str:
    bad_lines = {
        '.. raw:: html',
        '<figure class="wp-block-embed is-type-rich is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">',
        '.. container:: wp-block-embed__wrapper',
        '</figure>',
    }
    stripped = line.strip()
    if stripped in bad_lines or 'wp-block-embed' in stripped:
        return ''
    return line


def fix_internal_urls(path: str) -> None:
    fix_content(path, url_fix_fn)


def href_repl(m) -> str:
    text = m.group(1)
    href = m.group(2)
    domains = { 'aftermathsgr.wordpress.com', 'aftermaths.gr' }
    DOCS_ROOT = 'docs'
    if any(x in href for x in domains):
        href_split = href.split('/')
        if href_split[-1]:
            target = href_split[-1]
        else:
            target = href_split[-2]
        target = unencode_filename(target) + '.rst'
        for dirpath, dirnames, filenames in os.walk(Config.CONTENT_STRUCT_DIR):
            if target in filenames:
                path_split = os.path.split(dirpath)
                content_index = path_split.index('__content') + 1
                dirs = os.path.join(path_split[content_index:])
                return f'`{text} <{os.path.join(dirs, target)}>`__'
    return f'`{text} <{href}>`__'


def url_fix_fn(line: str, params: dict=dict()) -> str:
    fixed_line = re.sub(r'`(.+)\s+<(.+)>`__', href_repl, line)
    return fixed_line


def fix_post_images(path: str) -> None:
    fix_content(path, post_img_fix_fn)


def post_img_fix_fn(line: str, params: dict=dict()) -> str:
    '''Remove foreign domain and dimension suffix'''
    fixed_line = re.sub(
        r'https://aftermaths.gr|\?w=\d+', r'', line
    )
    fixed_line = re.sub(r'\{static\}', r'/', fixed_line)
    return fixed_line


def fix_aligned_math(path: str) -> None:
    fix_content(path, alignment_fix_fn)


def alignment_fix_fn(line: str, params: dict=dict()) -> str:
    fixed_line = re.sub(r'(?:\\begin|\\end)\{align\}', r'', line)
    fixed_line = re.sub(r'(?<!\\)\\&', r'\\\\ &', fixed_line)
    return fixed_line


def fix_keraia(path: str) -> None:
    fix_content(path, keraia_fix_fn)


def keraia_fix_fn(line: str, params: dict=dict()) -> str:
    fixed_line = re.sub(r"(?<=\w)'", r'ʹ', line)
    return fixed_line


def remove_wp_code(path: str) -> None:
    fix_content(path, wp_remove_fn)


def wp_remove_fn(line: str, params: dict=dict()) -> str:
    fixed_line = re.sub(r'wp-block-syntaxhighlighter-code', r'', line)
    return fixed_line


def fix_tables(path: str) -> None:
    fix_content(path, table_fix_fn)


def table_fix_fn(line: str, params: dict=dict()) -> str:
    # If we are parsing a table, just consume the next line
    #if any(params.values()):
    #    print(params)
    # Check what we are parsing, i.e., table, caption or anything else
    # Check if we are parsing a table
    parsing_table = params.get('parsing_table')
    if parsing_table is None:
        params['parsing_table'] = False
        params['table_str'] = ''
    if re.match(r'^\s*\<figure class="wp-block-table.+"\>.*$', line):
        params['parsing_table'] = True
        params['table_str'] = '\t:widths: auto\n' # Caption / Title is prepended later.
        return ''
    # Check whether we are parsing a caption
    parsing_caption = params.get('parsing_caption')
    if parsing_caption is None:
        params['parsing_caption'] = False
        params['caption_str'] = ''
    if re.match(r'^\s*\<figcaption\>.*$', line):
        params['parsing_caption'] = True
        params['parsing_table'] = False
        return ''
    # Check if parsing has ended
    if re.match(r'^\s*\</figcaption\>.*$', line):
        params['parsing_caption'] = False
        return (
            f'.. table:: {params["caption_str"]}'
            f'{params["table_str"]}'
        )
    # Take cases accordingly
    if parsing_table:
        params['table_str'] = params['table_str'] + '\t' + line
        return ''
    # If we match a figcaption
    if parsing_caption:
        if re.match(r'.+', line.strip()):
            params['caption_str'] = params['caption_str'] + ' ' + line
        return ''
    return line


def remove_math_colour(path: str) -> None:
    fix_content(path, fix_math_colour_fn)


def fix_math_colour_fn(line: str, params: dict=dict()) -> str:
    fixed_line = re.sub(r'\&(?:fg|bg)=\w{6}\&(?:bg|fg)=\w{6}', r'', line)
    return fixed_line


def main():
    # rename_content()
    # restore_backups(Config.BACKUP_DIR, Config.CONTENT_DIR)
    # Fix content
    fnames = get_files_in_dir(Config.SPHINX_DOCS, "rst")
    # fnames = get_files_in_dir(Config.CONTENT_STRUCT_DIR, 'rst')
    # create_content_tree(Config.CONTENT_ROOT)
    for file_path in tqdm(map(os.path.abspath, fnames)):
        # fix_math_content(file_path)
        # fix_forward_slashes(file_path)
        # fix_video_urls(file_path)
        # fix_main_image(file_path)
        # fix_meta_content(file_path)
        # fix_raw_html_videos(file_path)
        # relocate_file(file_path)
        # fix_internal_urls(file_path)
        # fix_post_images(file_path)
        # fix_aligned_math(file_path)
        # fix_keraia(file_path)
        # remove_wp_code(file_path)
        # fix_tables(file_path)
        remove_math_colour(file_path)


if __name__ == "__main__":
    main()
