import requests
import time
import random
from bs4 import BeautifulSoup

def scrapper(filename):
    # URL = "https://www.greek-language.gr/digitalResources/literature/tools/concordance/browse.html?cnd_id=9&text_id=" ### Kavafis
    # URL = "https://www.greek-language.gr/digitalResources/literature/tools/concordance/browse.html?cnd_id=6&text_id=" ### Kariotakis
    URL = "https://www.greek-language.gr/digitalResources/literature/tools/concordance/browse.html?cnd_id=7&text_id=" ### Palamas
    poem_ids = [str(x) for x in range(1180, 2706)]
    data_str = ""
    try:
        for id in poem_ids:
            delay = 0.5 + random.random()
            time.sleep(delay)
            print(id, delay)
            poem_str = ""
            url = URL + id
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            lines = soup.find_all("span", class_ = "l")
            for line in lines:
                poem_str += line.text + "\n"
            data_str += poem_str + "\n"
    except:
        with open(filename, "w") as file:
            file.write(data_str)
    with open(filename, "w") as file:
        file.write(data_str)

def main():
    filename = "greek-language-scrap-palamas.txt"
    scrapper(filename)

if __name__ == "__main__":
    main()