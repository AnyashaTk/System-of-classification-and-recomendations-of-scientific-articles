import pandas as pd
import gensim
from matplotlib import pyplot
from numpy import unique, where
from sklearn.cluster import DBSCAN, Birch
from sklearn.datasets import make_classification

from utils import *
from constants import *

full_dataset = list(pd.read_csv(path)['0'].dropna())

train_tokenized = tokenize_corpus(full_dataset)

# print(train_tokenized[:5])

model = gensim.models.Word2Vec(sentences=train_tokenized, size=2, window=5,
                               min_count=1, workers=4,
                               iter=10)  # an empty model, no training yet

# print(model.most_similar('such'))

w2v_vectors = model.wv.vectors  # here you load vectors for each word in your model
w2v_indices = {word: model.wv.vocab[word].index for word in model.wv.vocab}
'''
sett = (vectorize(x, w2v_indices, w2v_vectors) for x in train_tokenized)
print(sett)

model1 = Birch(threshold=0.01, n_clusters=2)
# fit the model
yhat = model1.fit(model.wv.vectors)
# assign a cluster to eac
clusters = unique(yhat)
# create scatter plot for samples from each cluster
for cluster in clusters:
    # get row indexes for samples with this cluster
    row_ix = where(yhat == cluster)
    # create scatter of these samples
    print(row_ix)
# show the plot
pyplot.show()'''


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
            v = model[word]
            # print(v)
            if np.isnan(v).any():
                print(word, v)
            featureVec = featureVec + model[word]
        else:
            not_in_model.append(word)
    # Here we can see if some of the words are not in the model, if so, we cannot use them for the clustering
    print(not_in_model)
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
X = getAvgFeatureVecs(train_tokenized, model, 2)

