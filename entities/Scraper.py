# entities/Scraper.py
from Post import Post

class Scraper:
    def __init__(self, url: str) -> None:
        self._url = url

    def scrap(self) -> Post:
        pass
