import os

import pandas as pd
import pdftotext


def start_space_num(line):
    num = 0
    while num < len(line) and line[num] == " ":
        num += 1
    return num


file_names = sorted(os.listdir("../two_columns_files/pdf"))
# Load PDF file
for file_name in file_names:
    with open("../two_columns_files/pdf/" + file_name, "rb") as f:
        pdf = pdftotext.PDF(f)
    dfs = []
    for page in pdf:
        avr_spaces = 0
        page = page.split("\n")
        df = pd.DataFrame([[0] * 2] * len(page), columns=["text", "space_num"])
        for line_num, line in enumerate(page):
            space_num = start_space_num(line)
            avr_spaces += space_num
            df.loc[line_num] = line, space_num
        avr_spaces /= len(page)
        df.loc[len(page) - 1] = ["avr_spaces", avr_spaces]
        name_without_extension = file_name[:file_name.rfind(".")]
        dfs += [df]
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv("../two_columns_files/csv_source/" + name_without_extension + '.csv', index=False)

    # Read all the text into one string
    # print("\n\n".join(pdf))