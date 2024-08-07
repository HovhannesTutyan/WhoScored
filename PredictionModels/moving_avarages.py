import numpy as np

# Sales data for each week
sales = np.array([39, 44, 40, 45, 38, 43, 39]) # sales per each week

""" In fact, people who find it difficult to draw trendlines often will substitute them for MOVING AVARAGES.
In general, though, if the price is above a particular moving average, then it can be
said that the trend for that stock is up relative to that average and when the price is
below a particular moving average, the trend is down."""
def moving_average(data, window_size = 3):
    moving_averages = []
    for i in range(len(data) - window_size):
        window_average = np.mean(data[i:i + window_size])
        moving_averages.append(window_average)
    return moving_averages

moving_averages = moving_average(sales)                                             # F_4 = (39+44+40) / 3 = 41; F_5 = (44 + 40 + 45) / 3 = 43 and so on
forecast_errors = [sales[i + 3] - ma for i, ma in enumerate(moving_averages)]       # Actual - Forecast, F_4 = 45 - 41 = 4; F_5 = 38 - 43 = -5
absolute_errors = np.abs(forecast_errors)                                           # | Absolute error |
mean_absolute_deviation = np.mean(absolute_errors)                                  # Mean of absolute errors (4 + 5 + 2 + 3)/ 4 = 3.5
squared_errors = np.square(forecast_errors)                                         # Square of forecast errors (16, 5, 4, 9)
mean_squared_error = np.mean(squared_errors)                                        # Mean of squared errors (54 / 4 = 13.5)
absolute_percent_error = np.abs(forecast_errors / sales[3:]) * 100                  # F_4 = 4 / 45 * 100; F_5 = 5 / 38 * 100
mean_absolute_percent_error = np.mean(absolute_percent_error)                       # | Absolute error | / Actual error * 100%           
# Print the results
for i, ma in enumerate(moving_averages, start=4):
    print(f"F_{i} = {ma:.2f}")
print ("forecast_errors", forecast_errors)
print( "MED ", mean_absolute_deviation)
print(mean_absolute_percent_error)

