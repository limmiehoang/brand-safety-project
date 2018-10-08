import numpy as np
import pandas as pd
import model.model_config as cf
import pickle
import sys

from spider.spider import makeObservation

test_url = sys.argv[1]

# Make X_test
obs = makeObservation(test_url)
X_test = [obs]

# Load the classifier
with open(cf.TRAINED_MODEL, 'rb') as fid:
    classifier = pickle.load(fid)

# # Predicting the Test set results
y_pred = classifier.predict(X_test)

print('---Result---')
if y_pred == [0]:
    print('This is not an accident news.')
else:
    print('This is an accident news.')