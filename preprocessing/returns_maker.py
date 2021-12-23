###############################################
# Creates the filtered returns
###############################################

print(40*"=")
print("returns_maker")
print(40*"=")

#utilities
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import sys
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from matplotlib import style
style.use('fivethirtyeight')

#Set up paths
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)



## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()
sys.path.append(parentdir)
import config as c

#market capitalization data set up
marketcap = format(c.market_cap,'.0e')
df_market_cap = pd.read_csv(f'{path_data_processed}/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv', index_col=0)
df_market_cap_first = df_market_cap.iloc[:c.number_cryptos]

#date first
first_date = df_market_cap_first['first_date_marketcap'].tail(1).values
first_date = first_date[0]

#close price set up
df_close_adj = pd.read_csv(f'{path_data_processed}/close_price_crypto.csv', index_col=0)
df_close_adj = df_close_adj.loc[df_close_adj.index > first_date]
df_close_adj = df_close_adj.loc[:, df_market_cap_first['crypto_name']]


#returns set up & save
df_volume_adj = pd.read_csv(f'{path_data_processed}/volume_price_crypto.csv', index_col=0)
df_volume_adj = df_volume_adj.loc[df_volume_adj.index > first_date]
df_volume_adj = df_volume_adj.loc[:, df_market_cap_first['crypto_name']]

df_returns = df_close_adj.pct_change().iloc[1:]
df_returns.replace(np.inf, 0, inplace=True)
df_returns.fillna(0, inplace=True)
df_returns.to_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#metrics set up
df_volume_adj.to_csv(f"{path_data_processed}/volume_first_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#metrics creation

df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'volatility', 'sharpe', 'excReturns', 'beta', 'max_drawdown', 'TE', 'IR', 'monthly_turnover', 'HHI'],
    index=['CW', 'BTC', 'EW', 'MV', 'Low Vol', 'High Vol', 'Low Beta', 'High Beta', 'Low Beta EW', 'High Beta EW', 'Low Beta BTC', 'High Beta BTC'])

df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#metrics for rebalanced set up
df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'volatility', 'sharpe', 'excReturns', 'beta', 'max_drawdown', 'TE', 'IR', 'monthly_turnover'],
    index=['CW', 'BTC', 'EW', 'MV', 'Low Vol', 'High Vol', 'Low Beta', 'High Beta', 'Low Beta EW', 'High Beta EW', 'Low Beta BTC', 'High Beta BTC'])

df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'volatility', 'sharpe', 'excReturns', 'beta', 'max_drawdown', 'TE', 'IR', 'monthly_turnover'],
    index=['CW', 'BTC', 'EW', 'MV', 'Low Vol', 'High Vol', 'Low Beta', 'High Beta', 'Low Beta EW', 'High Beta EW', 'Low Beta BTC', 'High Beta BTC'])

df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
