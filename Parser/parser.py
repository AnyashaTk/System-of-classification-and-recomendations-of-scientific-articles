from parser_config import *
from parser_funcs import *

file_names = save_files(BASE_DATA_PATH, "astro-ph", CSV_SAVE_PATH, num_files=20, return_csv_names=True)
file_names = os.listdir("../csv_data")
for file_name in file_names[:10]:
    df = pd.read_csv(CSV_SAVE_PATH + file_name)
    df = df.loc[df["fonts-type"] != "Times-Roman"]
    df.to_csv("")
