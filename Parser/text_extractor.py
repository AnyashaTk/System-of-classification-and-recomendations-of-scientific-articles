import pandas as pd
import tika
import os

tika.initVM()
from tika import parser
os.chdir("../")
for file_name in sorted(os.listdir("../PDF_data/astro-ph"))[:200]:
    rpoint = file_name.rfind(".")
    name_without_extension = file_name[:rpoint]
    parsed = parser.from_file('../PDF_data/astro-ph/' + file_name)
    s = pd.Series([(line if len(line) > 5 else None) for line in parsed["content"].split("\n\n")]).dropna()
    s.to_csv("./csv_text_data/"+name_without_extension+".csv", index=False)
