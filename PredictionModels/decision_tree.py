import pandas as pd
from sklearn import tree
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, classification_report

data = load_breast_cancer()
dataset = pd.DataFrame(data=data['data'], columns=data['feature_names'])

x = dataset.copy() # all data available
y = data['target'] # either 0 or 1 (good or bad)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33) # take 33% for testing

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
accuracy_score(y_test, predictions)
confusion_matrix(y_test, predictions, labels=[0,1])
precision_score(y_test, predictions)
classification_report(y_test, predictions, target_names=['malignant', 'bening'])

feature_names = x.columns
feature_importance = pd.DataFrame(clf.feature_importances_, index=feature_names).sort_values(0,ascending=False)
features = list(feature_importance[feature_importance[0]>0].index)
feature_importance.head(10).plot(kind='bar')
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(clf, feature_names=feature_names, class_names={0:'Malignant', 1:'Bening'}, filled=True, fontsize=12)
plt.show()
