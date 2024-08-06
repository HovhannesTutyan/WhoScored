import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from matplotlib import pyplot as plt
solana_data = [
    {
        "name": "Solana",
        "symbol": "SOL",
        "date": "2023-07-26",
        "price_usd": 23.267716629540782,
        "market_cap": 9395875459.492481,
        "volume_24h": 362056307.62913954
    },
    {
        "name": "Solana",
        "symbol": "SOL",
        "date": "2023-07-27",
        "price_usd": 25.1519878372353,
        "market_cap": 10171319431.282724,
        "volume_24h": 682755887.4427278
    },
    {
        "name": "Solana",
        "symbol": "SOL",
        "date": "2023-07-28",
        "price_usd": 25.093488053679394,
        "market_cap": 10151894149.311943,
        "volume_24h": 493788462.55482113
    },
    {
        "name": "Solana",
        "symbol": "SOL",
        "date": "2023-07-29",
        "price_usd": 24.825803970620775,
        "market_cap": 10051629238.612888,
        "volume_24h": 354454914.9621894
    }
]

btc_data = [
    {
        "name": "Bitcoin",
        "symbol": "BTC",
        "date": "2024-07-21",
        "price_usd": 67206.06470614894,
        "market_cap": 1325658979467.9998,
        "volume_24h": 17353396168.041622
    },
    {
        "name": "Bitcoin",
        "symbol": "BTC",
        "date": "2024-07-22",
        "price_usd": 68088.13996324532,
        "market_cap": 1343346742483.077,
        "volume_24h": 27078771827.95196
    },
    {
        "name": "Bitcoin",
        "symbol": "BTC",
        "date": "2024-07-23",
        "price_usd": 67607.71339918874,
        "market_cap": 1333201881091.7786,
        "volume_24h": 43157593651.80313
    },
    {
        "name": "Bitcoin",
        "symbol": "BTC",
        "date": "2024-07-24",
        "price_usd": 65829.05554998077,
        "market_cap": 1298045800967.5593,
        "volume_24h": 24463772177.295467
    }
]

"""Simple daily percentage change
daily_percentage_change = (change_amount_today / change_amount_yesterday) - 1
"""
def daily_perc_change(data):
    df = pd.DataFrame(data)
    df['percentage_change'] = ((df['price_usd'] / df['price_usd'].shift(1)) - 1) * 100
    return df

"""Simple daily cumulative returns
This informs us that the value of $1 invested in SOL on 2023-07-26 would be worth
$1.06 on 2023-07-29.
"""

def daily_cumulative_returns(perc_change_data):
    df = pd.DataFrame(perc_change_data)
    df['cum_daily_return'] = (1 + df['percentage_change'] / 100).cumprod()
    return df

daily_change_sol = daily_perc_change(solana_data)
daily_change_btc = daily_perc_change(btc_data)
cum_return = daily_cumulative_returns(daily_change_sol)
# print(cum_return[['date', 'price_usd', 'percentage_change','cum_daily_return']])
# cum_return['cum_daily_return'].plot(figsize=(12,8))
# plt.legend(loc=2)
# cum_return['percentage_change'].describe()
# f = plt.figure(figsize=(12,8))
# ax = f.add_subplot(111)
# stats.probplot(df['cum_daily_return'], dist='norm', plot=ax)
# plt.show()

"""Comparison of daily percentage change between stocks. The more amount of correlation between 2 stocks, the more dots will be near the horizontal slope."""

def render_scatter_plot(x_stock_change, y_stock_change, xlim=None, ylim=None):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.scatter(x_stock_change, y_stock_change, color='blue')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.autoscale(False)
    ax.vlines(0, -10, 10, color='gray', linestyles='dashed')
    ax.hlines(0, -10, 10, color='gray', linestyles='dashed')
    ax.plot((-10, 10), (-10, 10))
    ax.set_xlabel('Daily percentage change Bitcoin')
    ax.set_ylabel('Daily percentage change Solana')
    ax.set_title('Comparison of Daily Percentage Change')
    plt.grid(True)
    
limits = [-10, 10]

render_scatter_plot(daily_change_btc['percentage_change'], daily_change_sol['percentage_change'], xlim=limits)
# plt.show()

"""Volatility calculation - a measurement of the change in variance in the returns of a stock over a specific period of time.
Volatility is calculated by taking a rolling window standard deviation on the
percentage change in a stock."""

def volatility_calc(data, window=75):
    rolling_std = data.rolling(window=window, min_periods=1).std()
    volatility = rolling_std * np.sqrt(window)
    return volatility

volatility_btc = volatility_calc(daily_change_btc['percentage_change'])
volatility_sol = volatility_calc(daily_change_sol['percentage_change'])
print('volatility_btc', volatility_btc, 'volatility_sol', volatility_sol)

"""Least-squares regression of returns. Considering the change in the volatility between two investments.."""

x = daily_change_btc['percentage_change'].dropna()
y = daily_change_sol['percentage_change'].dropna()
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
print(model.summary())
