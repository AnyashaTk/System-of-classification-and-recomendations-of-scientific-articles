import pandas as pd

import urllib.request

df = pd.read_csv("arxiv_links.csv")
for ind in list(df.index):
    url, folder_name = df.url[ind], df["type"][ind]
    print(url, folder_name)
    file_name=url.split("/")[-1]
    urllib.request.urlretrieve(url,
                           '/home/stork/PycharmProjects/System-of-classification-and-recomendations-of-scientific-articles/PDF_data/'+folder_name+"/"+file_name+".pdf")
