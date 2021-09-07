import os

import pandas as pd


def is_double_columns(line: str) -> bool:
    line = line.strip()
    if "   " in line:
        return True
    return False


def get_words_from_line(line: str):
    words = [word if word.strip() != '' else None for word in line.strip().split(" ")]
    while None in words:
        words.remove(None)
    return words


SAVE_DIR = "./csv_parsed/"
SOURCE_PATH = "./csv_source/"
COLUMNS_NAME = ["symbolic_percent", "space_percent", "num_world", "num_columns", "front_spaces_perc", "back_spaces"]

file_names = sorted(os.listdir(SOURCE_PATH))
# нахождение базовых
for file_name in file_names:
    df = pd.read_csv(SOURCE_PATH + file_name)
    df_text = df["text"]
    # данные о всем документе
    max_line_len = max([len(line) for line in list(df_text)])
    data_df = pd.DataFrame(
        columns=COLUMNS_NAME)
    for num, line in enumerate(df_text):
        # данные о словах
        words = get_words_from_line(line)
        # данные о строке
        symbolic_line = line
        while " " in symbolic_line: symbolic_line = symbolic_line.replace(" ", "")
        symbolic_percent = len(symbolic_line) / len(line)
        space_percent = 1 - symbolic_percent
        num_world = len(words)
        num_columns = len(line.strip().split("  "))
        front_spaces_perc = df["space_num"][num] / max_line_len
        back_spaces = 1 - len(line) / max_line_len
        df_line = dict(zip(
            COLUMNS_NAME, [symbolic_percent, space_percent, num_world, num_columns, front_spaces_perc, back_spaces]))
        data_df = data_df.append(df_line, ignore_index=True)

    df_with_data = df.join(data_df)
    name_without_extension = file_name[:file_name.rfind(".")]
    df_with_data.to_csv(SAVE_DIR + name_without_extension + "_data.csv", index=False)
