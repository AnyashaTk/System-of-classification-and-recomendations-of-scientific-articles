from utils import *
from constants import *
#from pipline import *
from sklearn.cluster import KMeans
import csv

#mod = pipline()
files_names = [file for file in os.listdir(path) if file.endswith(".csv")]
data, texts = get_many_columns(files_names)

model = KMeans(n_clusters=50)
# fit the model
model.fit(data)
# assign a cluster to each example
yhat = model.predict(data)

file_name = "clusters.csv"
dictionary = pd.DataFrame({'text': texts[0], 'claster': yhat})
row1 = "text"
row2 = "cluster"
# here will be a cycle
def write_csv(file_name, row1, row2, dictionary):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((row1, row2))
        for i in dictionary.index:# _, key, value
            key = dictionary["text"][i]
            value = dictionary["claster"][i]
            writer.writerow([key, value])


write_csv(file_name, row1, row2, dictionary)
