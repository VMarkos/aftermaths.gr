import sys
import os
import re
import json
from typing import Union

"""
TODO: \\tor and \\tand are not properly subsituted, e.g., in a closed environment there is an issue.
TODO: Catch all "hmmm" environments and add colour to their math expressions!
TODO: Consider making `\footnote{}'s parenthetical comments (is this always right?).
    * Footnotes must be "decapitalised.
    * What about footnotes that come just before `$...$`? In that case, what about just moving them after `$...$`?
    * What about dots (.) in the end of footnotes? Should they always be removed?
TODO: Within tikz environments, keep `--` and do not add `latex ` before everything.
TODO: Automatically export any tikz pictures, adding the `xkcd` style where appropriate.
TODO: Consider substituting expressions like "Σχημα~\ref{...}" with a more appropriate phrase for a blog.
TODO: What about italics and bold? This practically means that we somehow meddle with WP's layout / HTML?
    * Study how WP represents its editor's blocks (muck like tags) and export directly to that format.
    * What about images?
"""

class Document:
    def __init__(self, content: str, encoding = "utf-8", config_file: str = "config.json") -> None:
        self.content: str = content
        self._preamble: str = ""
        self._encoding: str = encoding
        self._original_content: str = content
        with open(config_file, "r") as file:
            self._params = json.load(file)
        self._strip_content()

    def _strip_content(self) -> None:
        begin_start = self.content.index(self._params["_LATEX_BEGIN_DOCUMENT"]) + len(self._params["_LATEX_BEGIN_DOCUMENT"])
        end_start = self.content.index(self._params["_LATEX_END_DOCUMENT"])
        self._preamble = self.content[:begin_start]
        self.content = self.content[begin_start:end_start]

    def _replace_dollars(self) -> None:
        is_starting = True
        i = 0
        while i < len(self.content):
            char = self.content[i]
            if char == self._params["_WP_EQN_DELIM"] and is_starting:
                self.content = self.content[:i + 1] + self._params["_LATEX"] + self.content[i + 1:]
                is_starting = False
                i += len(self._params["_LATEX"])
            elif char == self._params["_WP_EQN_DELIM"] and not is_starting:
                is_starting = True
            i += 1

    def _replace_equations(self) -> None:
        i = 0
        while i < len(self.content) - 1:
            delim = self.content[i:i + 2]
            if delim == self._params["_LEFT_EQN"]:
                self.content = self.content[:i] + self._params["_LEFT_EQN_LATEX"] + self.content[i + 2:]
                i += len(self._params["_LEFT_EQN_LATEX"])
            elif delim == self._params["_RIGHT_EQN"]:
                self.content = self.content[:i] + self._params["_WP_EQN_DELIM"] + self.content[i + 2:]
                i += len(self._params["_RIGHT_EQN"]) + len(self._params["_WP_EQN_DELIM"]) - 1
            i += 1

    def _replace_alignment(self) -> None:
        self.content = self.content.replace("align*", "aligned")
        self.content = self.content.replace("\\begin{aligned}", self._params["_WP_EQN_DELIM"] + self._params["_LATEX"] + "\\begin{aligned}")
        self.content = self.content.replace("\\end{aligned}", "\\end{aligned}" + self._params["_WP_EQN_DELIM"])

    def __encode_str(self, string) -> str:
        return string.encode(self._encoding).decode(self._encoding)

    def _replace_misc_symbols(self) -> None:
        self.content = self.content.replace("\\ldots", self.__encode_str("..."))
        self.content = self.content.replace("\\tor", self.__encode_str("$ ή $" + self._params["_LATEX"]))
        self.content = self.content.replace("\\tand", self.__encode_str("$ και $" + self._params["_LATEX"]))
        self.content = self.content.replace("---", "-")
        self.content = self.content.replace("--", "-")
        self.content = self.content.replace("?", ";")

    def _replace_commands(self) -> None:
        commands = self.__extract_commands()
        for command in commands:
            # if command["arg_count"] == 0:
            #     self.content = self.content.replace(command["cmd_name"], command["cmd_body"])
            # else:
            self.__apply_command(command)

    def __apply_zero_args_command(self, cmd: dict) -> None:
        cmd_name = cmd["cmd_name"]
        cmd_body = cmd["cmd_body"]
        cmd_name_re = re.compile(r"\\" + cmd_name[1:] + r"[^a-zA-Z]|\\" + cmd_name[1:] + r"$")
        balance = 0
        step = len(cmd_body) - len(cmd_name)
        for match in re.finditer(cmd_name_re, self.content):
            start = match.start() + balance
            end = match.end() + balance - 1
            self.content = self.content[:start] + cmd_body + self.content[end:]
            balance += step
    
    def __apply_command(self, cmd: dict) -> None:
        if cmd["arg_count"] == 0:
            self.__apply_zero_args_command(cmd)
            return
        needle = cmd["cmd_name"] + "{"
        haystack_start = 0
        needle_index = self.content[haystack_start:].find(needle)
        start = needle_index + haystack_start
        while needle_index > -1:
            end = start + len(needle) - 1
            cmd_args, args_length = self.__extract_args(end, cmd["arg_count"])
            cmd_instance = self.__replace_args(cmd, cmd_args)
            self.content = self.content[:start] + cmd_instance + self.content[end + args_length:]
            haystack_start = end
            needle_index = self.content[haystack_start:].find(needle)
            start = needle_index + haystack_start
            
    def __replace_args(self, cmd: dict, cmd_args: list) -> str:
        cmd_instance = cmd["cmd_body"]
        for i in range(len(cmd_args)):
            cmd_instance = cmd_instance.replace(f"#{i + 1}", cmd_args[i])
        return cmd_instance

    def __extract_args(self, end: int, arg_count: int) -> list:
        occ_args = []
        parsing_arg = False
        balance = 0
        current_arg = ""
        i = 0
        while len(occ_args) < arg_count:
            char = self.content[end + i]
            if char == "{" and not parsing_arg:
                parsing_arg = True
                balance += 1
            elif char == "{":
                balance += 1
                current_arg += char
            elif char == "}" and balance == 1:
                occ_args.append(current_arg)
                current_arg = ""
                balance -= 1
                parsing_arg = False
            elif char == "}":
                balance -= 1
                current_arg += char
            elif parsing_arg:
                current_arg += char
            i += 1
        return occ_args, i

    def __extract_commands(self) -> list:
        lines = self._preamble.splitlines()
        commands = []
        for line in lines:
            if self._params["_NEWCOMMAND_HEADER"] not in line:
                continue
            cmd = self.__parse_command(line)
            if cmd is not None:
                commands.append(cmd)
        return commands

    def __parse_command(self, cmd_str: str) -> Union[dict, None]:
        cmd_str = cmd_str.strip()
        arg_count = 0
        if "[" in cmd_str:
            left_sqbr_index = cmd_str.index("[")
            right_sqbr_index = cmd_str.index("]")
            arg_count = int(cmd_str[left_sqbr_index + 1:right_sqbr_index])
        left_cubr_index = cmd_str.index("{")
        right_cubr_index = cmd_str.index("}")
        cmd_name = cmd_str[left_cubr_index + 1:right_cubr_index]
        if cmd_name.strip() in self._params["_CMD_BLACKLIST"]:
            return None
        body_lcubr_index = cmd_str[right_cubr_index:].index("{")
        cmd_body = cmd_str[right_cubr_index + body_lcubr_index + 1:-1]
        return {
            "cmd_name": cmd_name,
            "arg_count": arg_count,
            "cmd_body": cmd_body,
        }
    
    def _polish_environments(self) -> None:
        for env in self._params["_ENVIRONMENTS"]:
            self._polish_environment(environment = env)

    def _polish_environment(self, environment: str = "aligned") -> None:
        haystack_start = 0
        beginning = "\\begin{" + environment + "}"
        ending = "\\end{" + environment + "}"
        found = self.content[haystack_start:].find(beginning)
        i = 0
        while found > -1:
            start = haystack_start + found
            end = start + self.content[start:].find(ending)
            alignment_tbc = self.content[start:end + len(ending)]
            collapsed = re.sub(r"\s+", r" ", alignment_tbc)
            collapsed = re.sub(r"\\\\", r"\\\\\\\\", collapsed)
            collapsed = re.sub(r"\\{", r"\\\\{", collapsed)
            collapsed = re.sub(r"\\}", r"\\\\}", collapsed)
            self.content = self.content[:start] + collapsed + self.content[end + len(ending):]
            haystack_start = end + len(ending)
            found = self.content[haystack_start:].find(beginning)
            i += 1
            # if i > 15:
            #     break

    def convert(self) -> None:
        self._replace_commands()
        self._replace_dollars()
        self._replace_equations()
        self._replace_alignment()
        self._polish_environments()
        self._replace_misc_symbols()

def main():
    ENCODING = "utf-8"
    if len(sys.argv) > 2:
        raise ValueError(f"More arguments than required: {sys.argv}. Exactly one argument, target file path, is required")
    if len(sys.argv) < 2:
        raise ValueError(f"Less arguments than required: {sys.argv}. Exactly one argument, target file path, is required")
    targetpath = sys.argv[1]
    directory, filename_ext = os.path.split(targetpath)
    filename, extension = os.path.splitext(filename_ext)
    with open(targetpath, "r", encoding = ENCODING) as source_file:
        content = source_file.read()
    document = Document(content, encoding = ENCODING)
    document.convert()
    target_path = os.path.join(directory, filename)
    os.makedirs(target_path, exist_ok = True)
    trans_path = os.path.join(target_path, filename + ".txt")
    with open(trans_path, "w", encoding = ENCODING) as transcribed:
        transcribed.write(document.content)
    print(f"Transcribed! Transcription available at: {trans_path}.")

if __name__ == "__main__":
    main()