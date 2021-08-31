import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pandas


def get_lincs(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs(response.text, 'html.parser')
    urls = []
    for elem in soup.find_all('a', attrs={"title": "Download PDF"}):
        urls += ["https://arxiv.org" + elem["href"]]
    return urls


chapters = ["astro-ph",
            "cond-mat",
            "gr-qc",
            "hep-ex",
            "hep-lat",
            "hep-ph",
            "hep-th",
            "math-ph",
            "nlin",
            "nucl-ex",
            "nucl-th",
            "physics",
            "quant-ph",
            "math",
            "cs",
            "q-bio",
            "q-fin",
            "stat",
            "eess",
            "econ"]
dfs = []
for chapter in chapters:
    year = 21
    urls = []
    while 2000 - len(urls) > 0 and year > 0:
        url = "https://arxiv.org/list/" + chapter + "/" + str(year) + "?skip=0&show=2000"
        df = pd.DataFrame(columns=["url", "type"])
        urls += get_lincs(url)[:2000 - len(urls)]
        year -= 1
    df["url"] = urls
    df["type"] = [chapter] * len(urls)
    print(len(urls))
    dfs += [df]
df = pd.concat(dfs, ignore_index=True)
df.to_csv("arxiv_links.csv", index=False)
