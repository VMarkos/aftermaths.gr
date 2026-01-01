import os
import json
import time
from entities.Scraper import Scraper
from entities.Post import Post
from utils import ensure_path_exists

with open("post_urls.json", "r") as file:
    URLS = json.load(file)

PWD = os.path.abspath(os.path.dirname(__file__))
POSTS_DIR = ensure_path_exists(os.path.join(PWD, "posts"))


def main():
    for url in URLS:
        scraper = Scraper(url)
        post = scraper.scrap()
        # post.write(format_='latex', directory=POSTS_DIR) # Uses post name to write to file
        post.write(format_="json", directory=POSTS_DIR)  # To debug
        time.sleep(2)


if __name__ == "__main__":
    main()
