import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
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

from scipy.optimize import minimize
import config as c

#get first_date
marketcap = format(c.market_cap,'.0e')
df_market_cap = pd.read_csv(f'../data/processed/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv', index_col=0)
df_market_cap_first = df_market_cap.iloc[:c.number_cryptos]
first_date = df_market_cap_first['first_date_marketcap'].tail(1).values
first_date = first_date[0]

#get marketcaps
df_marketcap = pd.read_csv('../data/processed/market_cap_crypto.csv', index_col=0)
df_marketcap = df_marketcap.loc[df_marketcap.index > first_date]
df_marketcap = df_marketcap.loc[:, df_market_cap_first['crypto_name']]
df_marketcap['sum'] = df_marketcap.sum(axis=1)
print(df_marketcap.shape)

#weigths
df_weights = pd.DataFrame(index=df_marketcap.index, columns=df_marketcap.iloc[:, :-1].columns)
for col in df_marketcap.iloc[:, :-1].columns:
    df_weights.loc[:, col] = df_marketcap.loc[:, col]/df_marketcap['sum']
df_weights=df_weights.iloc[1:]

#plot bitcoin marketcap
fig = px.scatter(df_weights['bitcoin'], x=df_weights['bitcoin'].index, y='bitcoin', title="Bitcoin (% of market cap)",labels={'bitcoin': "% of market cap"})
fig.write_image(f"../plots/bitcoin_marketshare_{c.number_cryptos}.png", format='png')

#returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_returns_CW = df_returns * df_weights


#portfolio
df_perf = df_returns_CW.sum(axis=1)
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100

df_price.to_csv(f"../data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
