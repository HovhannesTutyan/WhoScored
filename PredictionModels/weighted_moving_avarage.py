import numpy as np

# Sales data for 7 weeks
sales = np.array([39, 44, 40, 45, 38, 43, 39]) # sales by each week

# Weights for WMA
weights = np.array([2,3]) 
# weights = np.array([0.1,0.2,0.3,0.4])
wl = len(weights)
sl = len(sales)
# Function to calculate WMA
def calculate_wma(sales, weights):
    wma = []
    if sum(weights) == 1:
    # Loop through weeks where WMA can be calculated
        for i in range(wl, sl):
            weighted_sum = np.dot(weights, sales[i-wl:i])  # Apply weights
            wma.append(weighted_sum)
        return wma
    else:
        for i in range(wl, sl):
            weighted_sum = np.dot(weights, sales[i-wl:i]) / sum(weights)  # Apply weights
            wma.append(weighted_sum)
        return wma

# Calculate WMA for weeks 5, 6, 7
wma_results = calculate_wma(sales, weights)

absolute_errors = [abs(actual - forecast) for actual, forecast in zip(sales[wl:sl], wma_results)]

mean_absolute_deviation = np.mean(absolute_errors)

# Print results
for i, (wma, error) in enumerate(zip(wma_results, absolute_errors), start=wl+1):
    print(f"Week {i}: WMA = {wma:.2f}, Absolute Error = {error:.2f}")
print("Mean Absolute Deviation", mean_absolute_deviation)
"""mean absolute deviation for weights = np.array([2,3]) is smaller than for weights = np.array([0.1,0.2,0.3,0.4]), 
which indicates that these weights smoothen the line better."""