# entities/Post.py
import re
import os
import json
from datetime import date
# from Transcoder import Transcoder

class Post:
    def __init__(self, author: str, date: 'date', title: str, content: str) -> None:
        self._author = author
        self._date = date
        self._title = title
        self._content = content
        self.__valid_formats = {'latex', 'json'}

    @property
    def uuid(self) -> str:
        date = self._date.strftime('%d-%m-%Y')
        title = re.sub(r'\W+', r'_', self._title.strip())
        return f'{title}_{self._author}_{date}'

    def as_dict(self) -> dict[str, any]:
        return {
            'author': self._author,
            'date': self._date.strftime('%Y-%m-%dT%H:%M:%S'),
            'title': self._title,
            'content': str(self._content),
        }

    def write(self, format_='latex', directory='.') -> None:
        self.__verify_format(format_)
        match format_:
            case 'latex':
                pass
            case 'json':
                self.__write_as_json(directory)

    def __write_as_json(self, directory: str) -> None:
        TARGET_PATH = os.path.join(directory, self.uuid + '.json')
        with open(TARGET_PATH, 'w') as file:
            json.dump(self.as_dict(), file)

    def __verify_format(self, format_: str) -> None:
        if format_ not in self.__valid_formats:
            raise ValueError(f'Invalid format: "{format_}". '
                'Expected: {", ".join(self.__valid_formats)}'
            )
