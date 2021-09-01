import pandas as pd
import tika

tika.initVM()
from tika import parser
for name in os.listdir("")
parsed = parser.from_file('../PDF_data/astro-ph/2001.00018.pdf')
s = []
k = 0
for line in parsed["content"].split("\n\n"):
    print(len(line))
    if len(line) > 5:
        s += [line]
        print(line)
        print("_____________________________________________________")
    else:
        k += 1
s = pd.Series(s)
s.to_csv("ser.scv",index=False)
print(k)
print(s)
