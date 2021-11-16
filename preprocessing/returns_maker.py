print(40*"=")
print("returns_maker")
print(40*"=")

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
import plotly.express as px
import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
import config as c

marketcap = format(c.market_cap,'.0e')
df_market_cap = pd.read_csv(f'../data/processed/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv', index_col=0)
df_market_cap_first = df_market_cap.iloc[:c.number_cryptos]

first_date = df_market_cap_first['first_date_marketcap'].tail(1).values
first_date = first_date[0]


df_close_adj = pd.read_csv('../data/processed/close_price_crypto.csv', index_col=0)
df_close_adj = df_close_adj.loc[df_close_adj.index > first_date]
df_close_adj = df_close_adj.loc[:, df_market_cap_first['crypto_name']]
#print(df_close_adj.head(1).iloc[:, :6])

#print(len(df_close_adj))
df_returns = df_close_adj.pct_change().iloc[1:]
df_returns.replace(np.inf, 0, inplace=True)
df_returns.fillna(0, inplace=True)
#print(len(df_returns))

#print(df_returns.iloc[210:250])
df_returns.to_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#metrics creation
df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'volatility', 'sharpe', 'excReturns', 'beta', 'max_drawdown', 'TE', 'IR', 'Turnover'],
    index=['CW', 'EW', 'MV', 'Low Vol', 'High Vol', 'Low Beta', 'High Beta'])

df_metrics.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")
