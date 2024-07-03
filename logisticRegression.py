# Your goal is to find the logistic regression function 𝑝(𝐱) 
# such that the predicted responses 𝑝(𝐱ᵢ) are as close as
# possible to the actual response 𝑦ᵢ for each observation 𝑖 = 1, …, 𝑛.
# Remember that the actual response can be only 0 or 1 in binary classification problems!
# This means that each 𝑝(𝐱ᵢ) should be close to either 0 or 1. 
# That’s why it’s convenient to use the sigmoid function.
# https://realpython.com/logistic-regression-python/

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

x = np.arange(10).reshape(-1,1)
y = np.array([0,0,0,0,1,1,1,1,1,1])
model = LogisticRegression(solver='liblinear', random_state=0)
model.fit(x,y)
print(model.classes_)
print(model.intercept_)
print(model.coef_)
print(model.predict_proba(x))
print(model.predict(x))
print(model.score(x,y))
cm = confusion_matrix(y, model.predict(x))
print(cm)
fig, ax = plt.subplots(figsize=(8,8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0,1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0,1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range (2):
    for j in range (2):
        ax.text(j,i,cm[i,j], ha='center', va='center', color='red')
plt.show()