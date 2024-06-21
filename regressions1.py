import numpy as np
from sklearn.linear_model import LinearRegression

# Simple Linear Regression, Coeffficient of determination, Intercept, Slope 

x = np.array([5,15,25,35,45,55]).reshape((-1,1)) # for example, house size in sq.feat
y = np.array([5,20,14,32,22,38])                 # prices for houses
model=LinearRegression()
model.fit(x,y)
r_sq = model.score(x,y)
print(f"coefficient of determination: {r_sq}")  # R^2 - coefficient of determination: 0.7158756137479542 
print(f"intercept: {model.intercept_}")         # b0  - intercept 5.633 - response is 5,63 when the x is 0.
print(f"slope: {model.coef_}")                  # b1  - slope     [0.54]- response rises by 0.54 when x is increased by one.
# y_pred = model.intercept_ + model.coef_ * x
y_pred = model.predict(x)
print(f"predictid response: \n {y_pred}")       # predicted response [ 8.33333333 13.73333333 19.13333333 24.53333333 29.93333333 35.33333333]


 



