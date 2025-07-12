
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.ensemble import VotingClassifier
import warnings
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

df = pd.read_csv('crop_production.csv')

df
df.columns
df.rename(columns={'production': 'production', 'cseason': 'cseason'}, inplace=True)

sum_maxp = df["production"].sum()
df["percent_of_production"] = df["production"].map(lambda x:(x/sum_maxp)*100)


def apply_results(prod):
        if (float(prod) <= 3):
            return 0  # Not Recommended
        elif (float(prod) >= 3):
            return 1  # Recommended

df['label'] = df['percent_of_production'].apply(apply_results)
# df.drop(['label'], axis=1, inplace=True)
results = df['label'].value_counts()

cv = CountVectorizer()
X = df['cseason']
y = df['label']


X = cv.fit_transform(X)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
X_train.shape, X_test.shape, y_train.shape

print("Naive Bayes")

from sklearn.naive_bayes import MultinomialNB
NB = MultinomialNB()
NB.fit(X_train, y_train)
predict_nb = NB.predict(X_test)
naivebayes = accuracy_score(y_test, predict_nb) * 100
print(naivebayes)
print(confusion_matrix(y_test, predict_nb))
print(classification_report(y_test, predict_nb))


# SVM Model
print("SVM")
from sklearn import svm
lin_clf = svm.LinearSVC()
lin_clf.fit(X_train, y_train)
predict_svm = lin_clf.predict(X_test)
svm_acc = accuracy_score(y_test, predict_svm) * 100
print(svm_acc)
print("CLASSIFICATION REPORT")
print(classification_report(y_test, predict_svm))
print("CONFUSION MATRIX")
print(confusion_matrix(y_test, predict_svm))




Labeled_Data = 'Labeled_Data.csv'
df.to_csv(Labeled_Data, index=False)
df.to_markdown