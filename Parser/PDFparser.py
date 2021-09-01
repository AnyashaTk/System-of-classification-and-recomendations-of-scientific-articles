import os
import re
import subprocess
import pandas as pd
import nltk
from bs4 import BeautifulSoup
import tempfile
from pdfminer.pdftypes import LITERALS_JBIG2_DECODE

class PDFParser(object):
    pathToScript = '/home/stork/PycharmProjects/ClsRecArticles/SCRSA/Parser/pdf2txt.sh'
    tmp_dir = '/home/stork/PycharmProjects/ClsRecArticles/SCRSA/data'
    font_size_diff_range = 2
    min_title_len = 10

    def __init__(self, pdf_path: str, pdf_name: str, csv_save_path: str = "./", save_csv=True):
        # nltk.download('punkt')
        # nltk.download('wordnet')
        # nltk.download('stopwords')

        temp_name = pdf_name
        pathPDFinput = pdf_path
        pathHTMLoutput = os.path.join(PDFParser.tmp_dir,
                                      '{}.html'.format(temp_name))

        command = 'sh {} "{}" "{}"'.format(self.pathToScript, pathHTMLoutput,
                                           pathPDFinput)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        c=process.returncode
        assert process.returncode == 0

        html = open(pathHTMLoutput, 'r')
        soup = BeautifulSoup(html, features='lxml')

        font_spans = [data for data in soup.select('span') if
                      'font-size' in str(data)]
        output = []
        for i in font_spans:
            # extract fonts-size
            fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',
                                   str(i.get('style'))).group(2)
            # extract into font-family and font-style
            fonts_family = re.search(r'(?is)(font-family:)(.*?)(;)',
                                     str(i.get('style'))).group(2)
            # split fonts-type and fonts-style
            try:
                fonts_type = fonts_family.strip().split(',')[0]
                fonts_style = fonts_family.strip().split(',')[1]
            except IndexError:
                fonts_type = fonts_family.strip()
                fonts_style = None
            output.append((str(i.text).strip(), fonts_size.strip(), fonts_type,
                           fonts_style))
        if save_csv:
            # create dataframe
            self.df = pd.DataFrame(output,
                                   columns=['text', 'fonts-size', 'fonts-type',
                                            'fonts-style'])

            self.df['fonts-size'] = pd.to_numeric(self.df['fonts-size'])
            self.df['text'] = self.df['text'].apply(
                lambda x: re.sub(r'\(cid:\d+\)', '', x))

            self.df['base_str_len'] = self.df['text'].str.len()
            tmp_texts_series = self.df['text'].copy().apply(
                lambda x: x.rstrip().split('\n'))
            tmp_max_len = tmp_texts_series.apply(
                lambda x: max([len(line) for line in x])
            )
            self.df['max_str_len'] = tmp_max_len.copy()

            self.df.to_csv(csv_save_path + temp_name + ".csv", index=False)
