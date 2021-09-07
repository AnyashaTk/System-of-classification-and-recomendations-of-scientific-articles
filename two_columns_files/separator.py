import os

import pandas as pd


def is_double_columns(line: str) -> bool:
    line = line.strip()
    if "   " in line:
        return True
    return False


def get_words_from_line(line: str) -> list:
    words = [word if word.strip() != '' else None for word in line.strip().split(" ")]
    while None in words:
        words.remove(None)
    return words


def upper_perc(word: str) -> float:
    upper_count = 0
    for liter in word:
        upper_count += liter.isupper()
    return upper_count / len(word)


def lower_perc(word: str) -> float:
    lower_count = 0
    for liter in word:
        lower_count += liter.islower()
    return lower_count / len(word)


def digits_perc(word: str) -> float:
    digit_count = 0
    for liter in word:
        digit_count += liter.isdigit()
    return digit_count / len(word)


SAVE_DIR = "./csv_parsed_by_words/"
SOURCE_PATH = "./csv_source/"
COLUMNS_NAME = ["word", "word_len", "word_upper", "word_lower", "word_digits", "line_symbolic_percent",
                "line_space_percent",
                "line_num_world", "line_num_columns",
                "line_front_spaces_perc", "line_back_spaces"]

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
        # получение данных о словах
        for word in words:
            word_len = len(word)
            upper = upper_perc(word)
            lower = lower_perc(word)
            digits = digits_perc(word)
            df_line = dict(zip(
                COLUMNS_NAME,
                [word, word_len, upper, lower, digits, symbolic_percent, space_percent, num_world, num_columns,
                 front_spaces_perc, back_spaces]))
            data_df = data_df.append(df_line, ignore_index=True)

    name_without_extension = file_name[:file_name.rfind(".")]
    data_df.to_csv(SAVE_DIR + name_without_extension + "_data.csv", index=False)
