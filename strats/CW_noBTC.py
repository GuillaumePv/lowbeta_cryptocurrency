#message for makefile
print(40*"=")
print("CW noBTC")
print(40*"=")

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

import sys
sys.path.append('..')

import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30
marketcap = format(c.market_cap,'.0e')


#get first_date
df_market_cap = pd.read_csv(f'../data/processed/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv', index_col=0)
df_market_cap.drop(df_market_cap.index[df_market_cap['crypto_name'] == 'bitcoin'], inplace = True)
#print(df_market_cap.iloc[:c.number_cryptos])
df_market_cap_first = df_market_cap.iloc[:c.number_cryptos]
first_date = df_market_cap_first['first_date_marketcap'].tail(1).values
first_date = first_date[0]

#get marketcaps
df_marketcap = pd.read_csv('../data/processed/market_cap_crypto.csv', index_col=0)
df_marketcap = df_marketcap.loc[df_marketcap.index > first_date]
df_marketcap = df_marketcap.loc[:, df_market_cap_first['crypto_name']]
df_marketcap['sum'] = df_marketcap.sum(axis=1)

#weigths
df_weights = pd.DataFrame(index=df_marketcap.index, columns=df_marketcap.iloc[:, :-1].columns)
for col in df_marketcap.iloc[:, :-1].columns:
    df_weights.loc[:, col] = df_marketcap.loc[:, col]/df_marketcap['sum']
df_weights=df_weights.iloc[1:]


#returns
df_close_adj = pd.read_csv('../data/processed/close_price_crypto.csv', index_col=0)
df_close_adj = df_close_adj.loc[df_close_adj.index > first_date]
df_close_adj = df_close_adj.loc[:, df_market_cap_first['crypto_name']]

df_returns = df_close_adj.pct_change().iloc[1:]
df_returns.replace(np.inf, 0, inplace=True)
df_returns.fillna(0, inplace=True)
df_returns_CW = df_returns * df_weights

#portfolio
df_perf = df_returns_CW.sum(axis=1)
df_perf.to_csv(f"../data/processed/CW_noBTC_perf_{c.number_cryptos}_1e{marketcap[-1]}.csv") #for the low beta calc
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100
df_price.to_csv(f"../data/strats/CW_noBTC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
print(df_price.tail(3))

#rebalance 7 days
results_7 = createPortfolio7(df_weights, df_returns)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_price_7.to_csv(f"../data/strats/CW_noBTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights, df_returns)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_price_30.to_csv(f"../data/strats/CW_noBTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
