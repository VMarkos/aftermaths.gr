# entities/Scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from .Post import Post


class Scraper:
    def __init__(self, url: str) -> None:
        self._url = url

    def scrap(self) -> Post:
        page = requests.get(self._url)
        soup = BeautifulSoup(page.content, "html.parser")
        post_author_card = soup.find("span", class_="author vcard")
        post_author = post_author_card.find("a").text
        post_date_str = soup.find("time", class_="entry-date published updated").get(
            "datetime"
        )
        post_date = datetime.strptime(post_date_str.split("+")[0], "%Y-%m-%dT%H:%M:%S")
        post_content = soup.find("div", class_="entry-content")
        post_title = soup.find("h1", class_="entry-title").text
        post = Post(post_author, post_date, post_title, post_content)
        return post
