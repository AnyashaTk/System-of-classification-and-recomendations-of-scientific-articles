import pandas as pd
import gensim
import os
from matplotlib import pyplot
from numpy import unique, where
from sklearn.cluster import DBSCAN, Birch
from sklearn.datasets import make_classification

from utils import *
from constants import *

files_names = [file for file in os.listdir(path) if file.endswith(".csv")]
texts_all = [pd.read_csv(path + file)['0'].dropna() for file in files_names]
all_tokenized = [(tokenize_corpus(text)) for text in texts_all]
texts_like_one = []
for token_text in all_tokenized:
    for str in token_text:
        texts_like_one.append(str)



one_text = list(pd.read_csv(path_t)['0'].dropna())
one_text_tokenized = tokenize_corpus(one_text)

model = gensim.models.Word2Vec(sentences=texts_like_one, size=EMB_SIZE, window=5,
                               min_count=1, workers=4,
                               iter=10)  # an empty model, no training yet

# print(model.most_similar('such'))

w2v_vectors = model.wv.vectors  # here you load vectors for each word in your model
w2v_indices = {word: model.wv.vocab[word].index for word in model.wv.vocab}


def featureVecMethod(words, model, num_features):
    # Pre-initialising empty numpy array for speed
    featureVec = np.zeros(num_features, dtype="float32")
    nwords = 0
    # Converting Index2Word which is a list to a set for better speed in the execution.
    index2word_set = set(model.wv.index2word)
    not_in_model = []
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1
            v = model.wv[word]
            #print(v)
            if np.isnan(v).any():
                print(word, v)
            featureVec = featureVec + model.wv[word]
        else:
            not_in_model.append(word)
    if not_in_model:
        # Here we can see if some of the words are not in the model, if so, we cannot use them for the clustering
        print('not_in_model', not_in_model)
    # Dividing the result by number of words to get average
    if nwords != 0:
        featureVec = featureVec / nwords
    return featureVec


def getAvgFeatureVecs(tweets, model, num_features):
    counter = 0
    tweetFeatureVecs = np.zeros((len(tweets), num_features), dtype="float32")
    #    all_tweets = len(tweets)
    for i, tweet in enumerate(tweets):
        #       # Printing a status message every 1000th review
        if counter % 1000 == 0:
            print("Review %d of %d" % (counter, len(tweets)))

        tweetFeatureVecs[counter] = featureVecMethod(tweet, model, num_features)
        counter = counter + 1
    return tweetFeatureVecs


# Calculate the vector matrix
X = getAvgFeatureVecs(one_text_tokenized, model, EMB_SIZE)

from sklearn.cluster import KMeans

# make the k-means model
NUM_CLUSTERS = 2
kmeans = KMeans(NUM_CLUSTERS, random_state=0, max_iter=100, n_init=1, verbose=True).fit_predict(X)
labels = list(kmeans)

# make a dictionary with tweets and labels
values = labels
keys = one_text
KMeans_clusters = dict(zip(keys, values))

import csv

# write a table
file_name = "clusters.csv"
dictionary = KMeans_clusters
row1 = "text"
row2 = "cluster"

# here will be a cycle
def writeCsv(file_name, row1, row2, dictionary):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((row1, row2))
        for key, value in dictionary.items():
            writer.writerow([key, value])


writeCsv(file_name, row1, row2, dictionary)

