# entities/Post.py
import re
from datetime import date
from Transcoder import Transcoder

class Post:
    def __init__(self, author: str, date: 'date', title: str, content: str) -> None:
        self._author = author
        self._date = date
        self._title = title
        self._content = content

    @property
    def post_uuid(self) -> str:
        date = self._date.strftime('%d-%m-%Y')
        title = re.sub(r'\s+', r'_', self._title)
        return f'{title}_{self._author}_{date}'

    def write(self, format='latex', directory='.') -> None:
        pass
