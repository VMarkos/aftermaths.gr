import os
import json
import time
from entities.Scraper import Scraper
from entities.Transcoder import Transcoder
from entities.Post import Post

with open('post_urls.json', 'r') as file:
    URLS = json.load(file)

PWD = os.path.abspath(os.path.dirname(__file__))
POSTS_DIR = os.path.join(PWD, 'posts')

def main():
    for url in URLS:
        post = Scraper.scrap(url)
        post.write(format='latex', directory=POSTS_DIR) # Uses post name to write to file
        time.sleep(2)

if __name__ == '__main__':
    main()
