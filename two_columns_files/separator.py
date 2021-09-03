import os

import pandas as pd


def is_double_columns(line: str) -> bool:
    line = line.strip()
    if "   " in line:
        return True
    return False


SAVE_DIR = "./csv_parsed/"
SOURCE_PATH = "./csv_source/"

file_names = sorted(os.listdir(SOURCE_PATH))[:1]
# нахождение базовых
for file_name in file_names:
    df = pd.read_csv(SOURCE_PATH + file_name)
    df_text = df["text"]
    max_line_len = max([len(line) for line in list(df_text)])
    for num, line in enumerate(df_text[100:150]):
        symbolic_line = line
        words = line.strip().split(" ")
        while " " in symbolic_line: symbolic_line = symbolic_line.replace(" ", "")
        sybolic_percent = len(symbolic_line) / len(line)
        space_percent = 1 - sybolic_percent
        num_world = line.strip().split(" ")
        num_columns = line.strip().split("  ")
        front_spaces_perc = df["space_num"][num] / max_line_len
        back_spaces = 1 - len(line) / max_line_len
        words = 
