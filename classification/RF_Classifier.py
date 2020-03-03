# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import numpy as np
from sklearn.model_selection import RandomizedSearchCV

train = 'train.csv'

print ("create train data")

df_train = pd.read_csv(train, sep = ',')
x_train = df_train.iloc[:, :-1]
y_train = df_train.iloc[:, -1]

train = 'test.csv'

print ("create test data")

df_test = pd.read_csv(train, sep = ',')
x_test = df_test.iloc[:, :-1]
y_test = df_test.iloc[:, -1]

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# Create a random forest Classifier. By convention, clf means 'Classifier'
clf = RandomForestClassifier()

clf_random = RandomizedSearchCV(estimator = clf, param_distributions = random_grid, n_iter = 20, cv = 3, verbose=2, random_state=42, n_jobs = -1)

# Train the Classifier to take the training features and learn how they relate
# to the training y (the species)
clf_random.fit(x_train, y_train)

print("Best score on the training set")
print(clf_random.best_score_)
print("Actual score on the testing set")
metrics.accuracy_score(y_test,preds)