import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Define tickers
sol_ticker = 'SOL-USD'
btc_ticker = 'BTC-USD'

# Load data with yfinance
try:
    sol_data = yf.download(sol_ticker, start='2019-01-01', end='2023-01-01')
    btc_data = yf.download(btc_ticker, start='2019-01-01', end='2023-01-01')
except Exception as e:
    print(f"Error fetching data: {e}")
    sol_data = pd.DataFrame()
    btc_data = pd.DataFrame()

# Check if data is loaded correctly
if sol_data.empty or btc_data.empty:
    print("Data loading failed. Exiting...")
else:
    # Select relevant columns and rename for clarity
    sol_data = sol_data[['Close', 'Volume']]
    sol_data.columns = ['SOL_Close', 'SOL_Volume']

    btc_data = btc_data[['Close', 'Volume']]
    btc_data.columns = ['BTC_Close', 'BTC_Volume']

    # Combine data into a single DataFrame
    data = pd.concat([sol_data, btc_data], axis=1).dropna()

    # Display the first few rows of the data
    print(data.head())

    # # Define features and target
    # X = data[['SOL_Close', 'SOL_Volume']]  # Features
    # y = data['BTC_Close']  # Target

    # # Split data into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # # Scale the data
    # scaler = StandardScaler()
    # X_train_scaled = scaler.fit_transform(X_train)
    # X_test_scaled = scaler.transform(X_test)

    # # Define models
    # models = {
    #     'LinearRegression': LinearRegression(),
    #     'Lasso': Lasso(),
    #     'ElasticNet': ElasticNet(),
    #     'DecisionTreeRegressor': DecisionTreeRegressor(),
    #     'KNeighborsRegressor': KNeighborsRegressor(),
    #     'SVR': SVR(),
    #     'RandomForestRegressor': RandomForestRegressor(),
    #     'GradientBoostingRegressor': GradientBoostingRegressor(),
    #     'ExtraTreesRegressor': ExtraTreesRegressor(),
    #     'AdaBoostRegressor': AdaBoostRegressor(),
    #     'MLPRegressor': MLPRegressor(max_iter=500)
    # }

    # # Evaluate models using cross-validation
    # results = {}
    # for name, model in models.items():
    #     try:
    #         cv_results = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
    #         results[name] = -cv_results.mean()
    #         print(f'{name}: Mean Squared Error = {results[name]:.4f}')
    #     except Exception as e:
    #         print(f'Error with model {name}: {e}')

    # # Fit the best model on the training data
    # best_model_name = min(results, key=results.get)
    # best_model = models[best_model_name]
    # best_model.fit(X_train_scaled, y_train)

    # # Predict on the test set
    # y_pred = best_model.predict(X_test_scaled)

    # # Evaluate the model
    # mse = mean_squared_error(y_test, y_pred)
    # print(f'{best_model_name} Test Mean Squared Error: {mse:.4f}')

    # # Feature Importance (if applicable)
    # if hasattr(best_model, 'feature_importances_'):
    #     feature_importances = best_model.feature_importances_
    #     features = X.columns
    #     feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
    #     print(feature_importance_df.sort_values(by='Importance', ascending=False))
