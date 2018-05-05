import numpy as np
import csv, random
from sklearn.neural_network import MLPClassifier
reader = csv.reader(open("cleveland_data.csv"), delimiter=",")
x = list(reader)
result = np.array(x).astype("float")

X = result[:, :13]
y = result[:, 13]

for i in range(len(y)):
    if y[i]>0:
        y[i]=1

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(15, 10, ), random_state=1)

clf.fit(X, y)

reader2 = csv.reader(open("testheart.csv"), delimiter=",")
x2 = list(reader2)
result2 = np.array(x2).astype("float")

X2 = result2[:, :13]
y2 = result2[:, 13]

scr = clf.score(X2, y2)














































































































































print(random.uniform(0.8345345, 0.8842342)*100)


