from parser_config import *


def save_files(data_path: str, modul: str, scv_save_path, num_files: int = 10, save_scv: bool = True,
               return_csv_names: bool = False):
    file_names = []
    for file_name in os.listdir(data_path + modul)[:num_files]:
        rpoint = file_name.rfind(".")
        name_without_extension = file_name[:rpoint]
        file_names += [name_without_extension + ".csv"]
        PDFParser(data_path + "astro-ph/" + file_name, name_without_extension, scv_save_path)
    if return_csv_names:
        return file_names
