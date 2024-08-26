import yfinance as yf
import numpy as np
import pandas as pd
import pyfolio as pf
import matplotlib.pyplot as plt

# setup the prarams
RISKY_ASSETS = ['AVAX-USD', 'SOL-USD', 'DOT-USD', 'MATIC-USD']
START_DATE = '2023-01-01'
END_DATE = '2023-01-10'
N_DAYS = 10
N_PORTFOLIOS = 10 ** 5

n_assets = len(RISKY_ASSETS)

# download the stock prices from Yahoo Finance
prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, auto_adjust=True)
prices_df['Close'].plot(title='Stock prices of the considered assets')
# plt.show()

# calculate individual asset returns
returns = prices_df['Close'].pct_change().dropna()

# define the weights, equal
portfolio_weights = n_assets * [1 / n_assets]

# calculate portfolio returns if the weight of assets is equal
portfolio_returns = pd.Series(np.dot(portfolio_weights, returns.T), index=returns.index)
print(f'If the weights of coins in the portfolio are equal, the returns of 25% each \n {returns} \n will be \n {portfolio_returns}')
# calculate annualized average returns and the corresponding standard deviation
avg_returns = returns.mean() * N_DAYS
cov_mat = returns.cov() * N_DAYS

# simulate random portfolio weights for 42 scenarios
np.random.seed(42)
weights = np.random.random(size=(N_PORTFOLIOS, n_assets))
weights /=  np.sum(weights, axis=1)[:, np.newaxis]

# calculate portfolio metrics

portf_rtns = np.dot(weights, avg_returns)
portf_vol = []
for i in range(0, len(weights)):
    portf_vol.append(np.sqrt(np.dot(weights[i].T, np.dot(cov_mat, weights[i]))))
portf_vol = np.array(portf_vol)
portf_sharpe_ratio = portf_rtns / portf_rtns

# crate a joint DataFrame with all data
portf_results_df = pd.DataFrame({'returns':portf_rtns,
                                  'volatility':portf_vol,
                                  'sharpe_ratio':portf_sharpe_ratio})

# Locate the points creating the Efficient Frontier

N_POINTS = 100
portf_vol_ef = []
indices_to_skip = []

portf_rtns_ef = np.linspace(portf_results_df.returns.min(), 
                            portf_results_df.returns.max(),
                            N_POINTS)
portf_rtns_ef = np.round(portf_rtns_ef, 2)                        
portf_rtns = np.round(portf_rtns, 2)
for point_index in range(N_POINTS):
    if portf_rtns_ef[point_index] not in portf_rtns:
        indices_to_skip.append(point_index)
        continue
    matched_ind = np.where(portf_rtns == portf_rtns_ef[point_index])
    portf_vol_ef.append(np.min(portf_vol[matched_ind]))

portf_rtns_ef = np.delete(portf_rtns_ef, indices_to_skip)

# plot the efficient frontier
MARKS = ['o', 'X', 'd', '*']

fig, ax = plt.subplots()
portf_results_df.plot(kind='scatter', x='volatility', 
                      y='returns', c='sharpe_ratio',
                      cmap='RdYlGn', edgecolors='black', 
                      ax=ax)
ax.set(xlabel='Volatility', 
       ylabel='Expected Returns', 
       title='Efficient Frontier')
ax.plot(portf_vol_ef, portf_rtns_ef, 'b--')
for asset_index in range(n_assets):
    ax.scatter(x=np.sqrt(cov_mat.iloc[asset_index, asset_index]), 
                y=avg_returns[asset_index], 
                marker=MARKS[asset_index], 
                s=150, 
                color='black',
                label=RISKY_ASSETS[asset_index])
ax.legend()

plt.tight_layout()
# plt.show()


# Maximum sharp portfolio with high volatility
max_sharpe_ind = np.argmax(portf_results_df.sharpe_ratio)
max_sharpe_portf = portf_results_df.loc[max_sharpe_ind]

min_vol_ind = np.argmin(portf_results_df.volatility)
min_vol_portf = portf_results_df.loc[min_vol_ind]

print('Maximum Sharpe Ratio portfolio ----')
print('\nPerformance')
for index, value in max_sharpe_portf.items():
    print(f'{index}: {100 * value:.2f}% ', end="", flush=True)
print('\nWeights')
for x, y in zip(RISKY_ASSETS, weights[np.argmax(portf_results_df.sharpe_ratio)]):
    print(f'{x}: {100*y:.2f}% ', end="", flush=True)

# Minimum volatility portfolio 
print('\nMinimum Volatility portfolio ----')
print('Performance')
for index, value in min_vol_portf.items():
    print(f'{index}: {100 * value:.2f}% ', end="", flush=True)
print('\nWeights')
for x, y in zip(RISKY_ASSETS, weights[np.argmin(portf_results_df.volatility)]):
    print(f'{x}: {100*y:.2f}% ', end="", flush=True)