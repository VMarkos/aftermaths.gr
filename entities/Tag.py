# entities/Tag.py

import html
from bs4.element import NavigableString, Tag


class Tag:
    def __init__(self, bs_tag) -> None:
        self.FLAT_TAGS = {"h2", "h3", "h4"}
        tag_name = bs_tag.name
        match tag_name:
            case w if w in self.FLAT_TAGS:
                self.__init_flat_tag(bs_tag)
            case "blockquote":
                ...
            case "p":
                self.__init_p_tag(bs_tag)
            case _:
                raise ValueError(f'Invalid tag name: "{tag_name}".')

    # TODO: Some tags need processing, so treat them separately, some others do not, e.g., headings, videos etc.

    def __init_flat_tag(self, bs_tag) -> None:
        self.name = bs_tag.name
        self.text = bs_tag.text
        self.attrs = dict()

    def __init_p_tag(self, p_tag) -> None:
        p_class = p_tag.get("class")
        if (
            p_class
            and "has-text-align-center" in p_class
            and len(p.contents) == 1
            and p_tag.find("img")
        ):  # is this correct?
            self.__init_display_math(p_tag)
        else:
            self.name = "p"
            self.text = "".join(TagUtils.parse_tag_contents(t) for t in p_tag.contents)
            self.attrs = dict()

    def __init_display_math(self, p_tag) -> None:
        img_tag = p_tag.find("img")
        self.name = "displaymath"
        self.text = TagUtils.parse_display_math(img_tag)
        self.attrs = dict()


class TagUtils:
    @staticmethod
    def parse_tag_contents(bs_tag) -> str:
        for c in bs_tag.contents:
            match type(c):
                case NavigableString:
                    return c.string
                case Tag:
                    return parse_nested_tag(bs_tag)
                case _:
                    raise ValueError(f'Unexpected element type: "{type(c)}".')

    @staticmethod
    def parse_nested_tag(bs_tag) -> str:
        match bs_tag.name:
            case "a":
                return parse_anchor_tag(bs_tag)
            case "img":
                return parse_inline_math(bs_tag)
            case "em":
                return parse_emphasis_tag(bs_tag)
            case "b":
                return parse_bold_tag(bs_tag)
            case "i":
                return parse_italics_tag(bs_tag)
            case _:
                raise ValueError(f'Unexpected nested tag: "{bs_tag.name}".')

    @staticmethod
    def parse_anchor_tag(a) -> str:
        href = a.get("href")
        text = a.text
        return "\\href{" + href + "}{" + text + "}"

    @staticmethod
    def parse_formatting_tag(bs_tag, formatting: str) -> str:
        return "\\" + formatting + "{" + bs_tag.text + "}"

    @staticmethod
    def parse_emphasis_tag(bs_tag) -> str:
        return parse_formatting_tag(bs_tag, "emph")

    @staticmethod
    def parse_bold_tag(bs_tag) -> str:
        return parse_formatting_tag(bs_tag, "textbf")

    @staticmethod
    def parse_italics_tag(bs_tag) -> str:
        return parse_formatting_tag(bs_tag, "textit")

    @staticmethod
    def parse_inline_math(img_tag) -> str:
        return "$" + parse_math_content(img_tag) + "$"

    @staticmethod
    def parse_display_math(img_tag) -> str:
        math_content = parse_math_content(img_tag)
        math_content.replace("\\displaystyle", "")
        return "\\[" + math_content + "\\]"

    @staticmethod
    def parse_math_content(img_tag) -> str:
        alt = img_tag.get["alt"]
        if alt is None:
            raise ValueError(f'Missing alt from math img tag "{img_tag}".')
        return html.unescape(alt)
