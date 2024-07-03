# Multiple linear regression

import numpy as np
from sklearn.linear_model import LinearRegression

x = [
  [0, 1], [5, 1], [15, 2], [25, 5], [35, 11], [45, 15], [55, 34], [60, 35]
]
y = [4, 5, 20, 14, 32, 22, 38, 43]
x, y = np.array(x), np.array(y)
model = LinearRegression().fit(x,y)
r_sq = model.score(x,y)
print(f"coefficient of determination: {r_sq}")  # R^2 - coefficient of determination: 0.8615939258756776 
print(f"intercept: {model.intercept_}")         # b0  - intercept 5.522 - response is 5,522 when the x is 0.
print(f"coefficients: {model.coef_}")           # b1  - coefficients     [0.45, 0.26]- increase of x1 by 1 yields a rise of the predicted response by 0.45, and x2 - 0.26.
y_pred = model.predict(x)
print(f"predictid response: \n {y_pred}")       #[ 5.77760476  8.012953   12.73867497 17.9744479  23.97529728 29.4660957 38.78227633 41.27265006]
