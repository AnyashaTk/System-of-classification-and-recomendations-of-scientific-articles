from PDFparser import PDFParser
import os
import pandas as pd

# Сброс ограничений на количество выводимых рядов
#pd.set_option('display.max_rows', 10)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', 100)
BASE_DATA_PATH = "/home/stork/PycharmProjects/System-of-classification-and-recomendations-of-scientific-articles/PDF_data/"
CSV_SAVE_PATH = "/home/stork/PycharmProjects/System-of-classification-and-recomendations-of-scientific-articles/SCRSA/csv_data/"