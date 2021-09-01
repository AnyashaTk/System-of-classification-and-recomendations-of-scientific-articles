import pandas as pd
import gensim
from utils import *
from constants import *

full_dataset = list(pd.read_csv(path)['0'].dropna())

train_tokenized = tokenize_corpus(full_dataset)

print(train_tokenized[:5])

model = gensim.models.Word2Vec(sentences=train_tokenized, size=100, window=5,
                               min_count=1, workers=4,
                               iter=10)  # an empty model, no training yet

'''
word2vec = gensim.models.Word2Vec(vocabulary, min_count=1)

word2vec = gensim.models.Word2Vec(sentences=train_tokenized, size=100,
                                  window=5, min_count=5, workers=4,
                                  sg=1, iter=10)'''

print(model.most_similar('galaxy'))
