from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats

url = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases"
    "/abalone/abalone.data"
)
## Get row data
abalone = pd.read_csv(url, header=None)
## Add header to the columns
abalone.columns = [
    'Sex',
    'Length',
    'Diameter',
    'Height',
    'Whole weight',
    'Shucked weight',
    'Visceria weight',
    'Shell weight',
    'Rings'
]
## Drop Sex as not phisical measure
abalone = abalone.drop('Sex', axis=1)
## Generate histogram, based on Rings (Count of Abalons by rings)
abalone["Rings"].hist(bins=15)
# plt.show()
## Find variable that has a strong correlation with aga except the rings.
correlation_matrix = abalone.corr()
correlation_matrix['Rings']

# Define distance on the vectors of the independent variables
# X is the independent variable, and y is the dependant variable.
X = abalone.drop("Rings", axis=1)
X = X.values
y = abalone["Rings"]
y = y.values

# Create a new data point of Abalone without Rings data
new_data_point = np.array([
    0.569552,
    0.446407,
    0.154437,
    1.016849,
    0.439051,
    0.222526,
    0.291208,
])
# Compute the distance between new data and each of the data points in Abalone Dataset.
distances = np.linalg.norm(X - new_data_point, axis=1)
# Find 3 closest neighbors to our new_data_point
k = 3
nearest_neighbor_ids = distances.argsort()[:k]

# Find the ground truths for these 3 neighbors (rings of the closest neighbors to our control data)
nearest_neighbor_rings = y[nearest_neighbor_ids]
# Calculate prediction for regression problems, that are numerical and average can be calculated
# that is 10, this means that for the control Abalone the rings count can be 10 based on same data neigbors
prediction = nearest_neighbor_rings.mean()
# Calculate the prediction for Classification problems, for example, car brands, mode is calculated (most often occuring value)
class_neighbors = y
## print(scipy.stats.mode(class_neighbors)) # mode=9, count=689
############
# Evaluate the model by splitting it to Training (neighbors) and Test (control) datas. test_size=0.2 means 20% of the original data for Test, and 80% of data for Training.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)
# Create model of the currect class, by using 3 nearest neighbors to predict the value of a future data point
knn_model = KNeighborsRegressor(n_neighbors=3)
# Fit the model on the training dataset
knn_model.fit(X_train, y_train)
# Evaluate the prediction error on the training data (Root mean square error)
train_preds = knn_model.predict(X_train)
mse = mean_squared_error(y_train, train_preds)
rmse = sqrt(mse)
## print(rmse)  1.65
# Evaluate the prediction error on the test data (Root mean square error)
test_preds = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
## print(rmse) 2.37 this measures the average error of the predicted age in years

# To understand what the model has learned, visualize the predictions
# Create a scatter plot of the first and second column of X_test (Length and Diameter)
cmap = sns.cubehelix_palette(as_cmap=True)
f, ax = plt.subplots()
points = ax.scatter(
    X_test[:, 0], X_test[:, 1], c=test_preds, s=50, cmap=cmap
)
f.colorbar(points)
# plt.show() # On the graph, each point is an abalone from the test set, with its actual length and diameter on X and Y respectively. The color is the predicted age. 
# The longer and larger an abalone is, the higher its predicted age.
# To confirm, whether this trend exists in actual abalone data, the same for the actual values can be done
## cmap = sns.cubehelix_palette(as_cmap=True)
## f, ax = plt.subplots()
## points = ax.scatter(
##     X_test[:, 0], X_test[:, 1], c=y_test, s=50, cmap=cmap
## )
## f.colorbar(points)
## plt.show() # this confirms that the trend exists

# Find the best value for K. GridSearchSV repeatedly fits KNN regressors on a part of the data and tests performance on the remaining part
parameters = {"n_neighbors":range(1, 50)}
gridsearch = GridSearchCV(KNeighborsRegressor(), parameters)
gridsearch.fit(X_train, y_train)
print(gridsearch.best_params_) # n_neighbors : 25 - choose 25 for value k will yield best predictive performance
# Use the gridsearch for evaluating the test data error as in row 78
train_preds_grid = gridsearch.predict(X_train)
train_mse = mean_squared_error(y_train, train_preds_grid)
train_rmse = sqrt(train_mse)
test_preds_grid = gridsearch.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
print(test_rmse)  # 2.17
print(train_rmse) # 2.07
# This means, our model fits less closely to the training data. Using GridSearchCV, you reduced the test RMSE from 2.37 to 2.17









