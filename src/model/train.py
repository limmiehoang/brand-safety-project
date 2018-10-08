# Random Forest Classification

# Importing the libraries
import numpy as np
import pandas as pd
import pickle
import model.model_config as cf
import os

# from sklearn.preprocessing import StandardScaler

# Importing the dataset
dataset = pd.read_csv(cf.DATASET)
X = dataset.iloc[:, :6000].values
y = dataset.iloc[:, 6000].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

# Fitting Random Forest Classification to the Training set
print('---Fitting Random Forest Classification to the Training set---')
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Save the classifier
exists = os.path.isfile(cf.TRAINED_MODEL)
if exists:
    os.rename(cf.TRAINED_MODEL, cf.TRAINED_MODEL + '.bk')

with open(cf.TRAINED_MODEL, 'wb') as fid:
    pickle.dump(classifier, fid)    
print('The classifier was saved to: ' + cf.TRAINED_MODEL)