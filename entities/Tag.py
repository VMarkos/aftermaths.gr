# entities/Tag.py

class Tag:
    def __init__(self, bs_tag) -> None:
        self.FLAT_TAGS = { 'h2', 'h3', 'h4' }
        tag_name = bs_tag.
        match name:
            case w if w in self.FLAT_TAGS:
                self.__init_flat_tag(name, text, attrs)
            case 'blockquote':
                ...

    # TODO: Some tags need processing, so treat them separately, some others do not, e.g., headings, videos etc.

    def __init_flat_tag(self, name: str, text: str, attr: dict[str, any])
        ...
        

