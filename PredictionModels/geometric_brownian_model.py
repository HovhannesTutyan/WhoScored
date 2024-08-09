import matplotlib.pyplot as plt
import warnings
import numpy as np
import pandas as pd
import yfinance as yf

# define params for downloading data
RISKY_ASSET = 'SOL-USD'
START_DATE = '2023-01-01'
END_DATE = '2023-07-31'

# download data from Yahoo finance
df = yf.download(RISKY_ASSET, start=START_DATE, end=END_DATE, auto_adjust=True)

# calculate daily returns
adj_close = df['Close']
returns = adj_close.pct_change().dropna()
ax = returns.plot()
ax.set_title(f'{RISKY_ASSET} returns: {START_DATE} - {END_DATE}', fontsize=16)
plt.tight_layout()
plt.show()
print(f'Absolute returns: {100 * returns}%')
print(f'Average return: {100 * returns.mean():.2f}%')

# split data into training and test sets
train = returns['2023-01-10' : '2023-06-30']
test = returns['2023-07-01' : '2023-07-31']

# specify the params of the test
T = len(train)
N = len(test)
S_0 = adj_close[train.index[-1]]
N_SIM = 100
mu = train.mean()
sigma = train.std()

# define the function used for simulation
def simulation_gbm(s_0, mu, sigma, n_sims, T, N, random_seed=42):
    """
    Function is user for simulating stock returns using Geometric Brownian Motion.
    Params
    ------
    s_0         - initial stock price
    mu          - drive coefficient
    sigma       - number of simulations paths
    dt          - time increment, most commonly a day
    T           - length of the forecast horizon, same unit as dt
    N           - number of time increments in the forecasting horizon
    random_seed - random seed for reproducibility

    Returns
    --------
    S_t         - matrix, containing the simulation results. rows are simple paths, columns are point of time.    
    """
    np.random.seed(random_seed)
    dt = T/N
    dW = np.random.normal(scale=np.sqrt(dt), size=(n_sims, N))
    W = np.cumsum(dW, axis=1)

    time_step = np.linspace(dt, T, N)
    time_steps = np.broadcast_to(time_step, (n_sims, N))
    S_t = s_0 * np.exp((mu - 0.5 * sigma**2) * time_steps + sigma * W)
    S_t = np.insert(S_t, 0, s_0, axis=1)
    return S_t

# run the simulations
gbm_simulations = simulation_gbm(S_0, mu, sigma, N_SIM, T, N)

# prepare objects for plotting
last_train_date = train.index[-1].date()
first_test_date = test.index[0].date()
last_test_date = test.index[-1].date()
plot_title = (f'{RISKY_ASSET} Simulation ' f'{first_test_date}:{last_test_date}')
selected_indices = adj_close[last_train_date:last_test_date].index
index = [date.date() for date in selected_indices]
gbm_simulations_df = pd.DataFrame(np.transpose(gbm_simulations), index=index)

# plotting
ax = gbm_simulations_df.plot(alpha=0.2, legend=False)
line_1, = ax.plot(index, gbm_simulations_df.mean(axis=1), color='red')
line_2, = ax.plot(index, adj_close[last_train_date:last_test_date], color='blue')
ax.set_title(plot_title, fontsize=16)
ax.legend((line_1, line_2), ('mean', 'actual'))
plt.tight_layout()
plt.show()
