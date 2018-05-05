import numpy as np
import csv, random
from sklearn import svm


reader = csv.reader(open("cleveland_data.csv"), delimiter=",")
x = list(reader)
result = np.array(x).astype("float")

X = result[:275, :13]
y = result[:275, 13]

clf = svm.SVC()
clf.fit(X, y)

reader2 = csv.reader(open("testheart.csv"), delimiter=",")
x2 = list(reader2)
result2 = np.array(x2).astype("float")


X2 = result[200:, :13]
y2 = result[200:, 13]

scr = clf.score(X2, y2)
print(scr*100)

