import os

import pandas as pd

for file_name in sorted(os.listdir("../PTT_first_pages"))[:3]:
    df = pd.read_csv("../PTT_first_pages/" + file_name)
    abstr_block_space_num = 150
    abstract_finded = False
    for inx in df.index:
        line = df["text"][inx]
        curr_spaces = df["space_num"][inx]
        a = abs(curr_spaces - abstr_block_space_num)
        if "ABSTRACT".lower() in line.lower():
            abstract_finded = True
            abstr_block_space_num = df["space_num"][inx + 1]
            a = abs(curr_spaces - abstr_block_space_num)
            curr_spaces = df["space_num"][inx+1]
        if abstract_finded and abs(curr_spaces - abstr_block_space_num) < 6:
            print(df["text"][inx])
            curr_spaces = df["space_num"][inx+1]
        else:
            abstract_finded = False
