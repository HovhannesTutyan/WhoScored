from collections import Counter
import matplotlib.pyplot as plt
from typing import List
import math 

def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)

num_friends = [
    100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,
    15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,
    10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,
    9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,
    7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,
    6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,
    5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
    4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
    3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
]

friends_count = Counter(num_friends)
xs = range(101)
ys = [friends_count[x] for x in xs]
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title('Histogram of friends count')
plt.xlabel('Count of friends')
plt.ylabel('Count of people')
# plt.show()
largest_value = max(num_friends)
smallest_value = min(num_friends)
sorted_values = sorted(num_friends)
smallest_value = sorted_values[0]
second_smallest_value = sorted_values[1]
second_largest_value = sorted_values[-2]

""" Central Tendencies calculations"""

def mean(x: List[float])->float:
    return sum(x) / len(x)
def median(v):
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2
    if n % 2 == 1:
        return sorted_v[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2
def quantile(x,p):
    p_index = int(p*len(x))
    return sorted(x)[p_index]
print("quantile(num_friends, 0.10)", quantile(num_friends, 0.10))
print("quantile(num_friends, 0.90)", quantile(num_friends, 0.90))
def mode(x):
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

""" Variations - scatter level of data. If 0, no scatter, if 1, full scatter. 
1. Difference of the min and max data
2. Mean deviation - average of the data's absolute deviation about the central point.
3. Standard Deviation - square root of the variance 
4. Variance - average squared deviation from the mean
5. Quartile Deviation - half of the difference between third and first quartile"""
def data_range(x: List[float]) -> float:
    return max(x) - min(x)
def de_mean(x: List[float])->List[float]:
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]
def variance(x: List[float]) -> float:
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n-1)
def standard_deviation(xs: List[float]) -> float:
    return math.sqrt(variance(xs))
def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

print(variance(friends_count))

"""Covariance - В отличие от дис-
персии, которая измеряет отклонение одной-единственной переменной от ее сред-
него, ковариация измеряет отклонение двух переменных в тандеме от своих сред-
них: функция dot суммирует произведения соответствующих пар эле-
ментов. Когда соответствующие элементы обоих векторов х и у одно-
временно выше или ниже своих средних, то в сумму входит положительное число.
Когда один из них находится выше своего среднего, а другой - ниже, то в сумму
входит отрицательное число. Следовательно, "большая" положительная ковариаuия
означает, что х стремится принимать большие значения при больших значениях у
и малые значения - при малых значениях у. "Большая" отрицательная ковариация
означает обратное - х стремится принимать малые значения при большом у, и на-
оборот. Ковариация, близкая к нулю, означает, что такой связи не существует."""

daily_minutes = [1,68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,
31.22,34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,
46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,31.21,36.32,
20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,24.23,21.4,27.94,
32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,
40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,
29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,
26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,
15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,35.59,39.43,
14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,20.9,21.9,18.79,27.61,27.21,
26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,
24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,
14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,
22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,
9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,
31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,
22.61,26.89,23.48,8.38,27.81,32.35,23.84]

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)

def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0
    
outlier = num_friends.index(100) # index of outlier

num_friends_good = [x
                    for i, x in enumerate(num_friends)
                    if i != outlier]

daily_minutes_good = [x
                      for i, x in enumerate(daily_minutes)
                      if i != outlier]

print("covariance(num_friends, daily_minutes)", covariance(num_friends, daily_minutes)) # 22.425435139573064
print("correlation(num_friends, daily_minutes)", correlation(num_friends, daily_minutes)) # 0.24736957366478218
print("correlation(num_friends_good, daily_minutes_good)", correlation(num_friends_good, daily_minutes_good))  # 0.5736792115665573 Outlier was lying