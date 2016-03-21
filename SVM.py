# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 16:22:49 2015

@author: Bohan Zhang
"""
import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.cross_validation import KFold
import os

filings = load_files('10-K')

X = np.array(filings.data)
y = np.array(filings.target)

negPath = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/extract report/10-K/neg'
posPath = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/extract report/10-K/pos'

N = len(os.listdir(negPath)) + len(os.listdir(posPath))
kf = KFold(N, n_folds=3)

accuracy = []
fold = 0

for train_index, test_index in kf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    vect = TfidfVectorizer()
    X_train_tfidf = vect.fit_transform(X_train)
    X_test_tfidf = vect.fit_transform(X_test)
        
    
    text_clf = Pipeline([("tfidf", TfidfVectorizer(sublinear_tf=True)),
                    ("svc", LinearSVC())])
    
    text_clf.fit(X_train, y_train)
    text_clf.predict(X_test)
        
    a= text_clf.score(X_test, y_test)
    
    accuracy.append(a)
    print '[INFO]\tFold %d Accuracy: %f' % (fold, a)
    fold += 1
    
avgAccuracy = sum(accuracy) / fold
print '[INFO]\tAccuracy: %f' % avgAccuracy    
