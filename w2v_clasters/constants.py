import collections
import re
import numpy as np

import pandas as pd
import gensim
import os
from matplotlib import pyplot
from numpy import unique, where
from sklearn.cluster import DBSCAN, Birch
from sklearn.datasets import make_classification

path1 = '/home/sparrow/Documents/GitHub/System-of-classification-and-recomendations-of-scientific-articles/csv_text_data/'
# path_t = '/home/sparrow/Documents/GitHub/System-of-classification-and-recomendations-of-scientific-articles/csv_text_data/2001.00018.csv'
path = '/home/sparrow/Documents/GitHub/System-of-classification-and-recomendations-of-scientific-articles/two_columns_files/csv_parsed/'

EMB_SIZE = 15
