import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# set random seed for reproducability
seeds = np.random.seed(42)

# define the params that will be used for this exercise
RISKY_ASSETS = ['BTC-USD', 'SOL-USD']
SHARES = [5, 5]
START_DATE = '2024-02-01'
END_DATE = '2024-02-10'
T = 1
N_SIMS = 10 ** 5

# download data from Yahoo finance
df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, auto_adjust=True)

adj_close = df['Close']
print(adj_close)
returns = adj_close.pct_change().dropna()
plot_title = f'{" vs ".join(RISKY_ASSETS)} returns: {START_DATE} - {END_DATE}'
returns.plot(title=plot_title)
plt.tight_layout()
cov_mat = returns.cov() # Variance is the dispersion around the mean. Positive covariance tells that when btc rises, sol rises along it
plt.show()
print(f'Correlation between returns: {returns.corr().values[0,1]:.2f}')
print(f'Covariance matrix will be {cov_mat}')

# perform the Cholesky decomposition of the covariance matrix, showing that random variables are correlated in the same way
chol_mat = np.linalg.cholesky(cov_mat)


# draw correlated random numbers from Standard Normal distribution
rv = np.random.normal(size=(N_SIMS, len(RISKY_ASSETS)))
correlated_rv = np.transpose(np.matmul(chol_mat, np.transpose(rv)))

# define metrics used for simulations
r = np.mean(returns, axis=0).values
sigma = np.std(returns, axis=0).values
S_0 = adj_close.values[-1, :]
P_0 = np.sum(SHARES * S_0)

# calculate the Terminal Price of the considered stocks
S_T = S_0 * np.exp((r-0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * correlated_rv)

# calculate the terminal portfolio value and the portfolio returns
P_T = np.sum(SHARES * S_T, axis=1)
P_diff = P_T - P_0

#calculate VaR
P_diff_sorted = np.sort(P_diff)
percentiles = [0.01, 0.1, 1.]
var = np.percentile(P_diff_sorted, percentiles)

for x, y in zip(percentiles, var):
    print(f'1-day VaR with {100-x}% confidence: {-y:.2f}$')

#present the results on a graph
ax = sns.distplot(P_diff, kde=False)
ax.set_title('''Distribution of possible 1-day changes in portfolio value 
             1-day 99% VaR''', fontsize=16)
ax.axvline(var[2], -100, 100)

plt.tight_layout()
plt.show()
var = np.percentile(P_diff_sorted, 5)
expected_shortfall = P_diff_sorted[P_diff_sorted<=var].mean()
# VaR (Value at Risk) indicates the maximum expected loss over a given time period at a certain confidence level
# for example, a 1-day var with 99% confidence tells that there is 1% chance the portfolio will lose more than this amount in one day
print(f'The 1-day 95% VaR is {-var:.2f}$, and the accompanying Expected Shortfall is {-expected_shortfall:.2f}$.')