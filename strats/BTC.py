#message for makefile
print(40*"=")
print("BTC")
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


from pathlib import Path

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]

path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

import sys
sys.path.append(parentdir)

import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30, getHerfindahl
marketcap = format(c.market_cap,'.0e')

#returns
df_close = pd.read_csv('../data/processed/close_price_crypto.csv', index_col=0)
df_close = df_close.loc[:, "bitcoin"]

df_returns = df_close.pct_change()
df_returns.replace(np.inf, 0, inplace=True)
df_returns.fillna(0, inplace=True)
df_returns.to_csv(f"../data/processed/BTC_perf_{c.number_cryptos}_1e{marketcap[-1]}.csv") #for the low beta calc

#weights
df_weights = df_returns.copy()
df_weights.iloc[:] = 1

#portfolio
df_returns[0] = 0
df_price = df_returns.add(1).cumprod()*100
df_price.to_csv(f"../data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
#turnover
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_metrics.loc["BTC", "monthly_turnover"] = 0
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#Herfindahl
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_metrics.loc["BTC", "HHI"] = 1
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#rebalance 7 days
df_price_7 = df_price
turnover_monthly_7 = 0
df_price_7.to_csv(f"../data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
#turnover
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics.loc["BTC", "monthly_turnover"] = 0
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
df_price_30 = df_price
turnover_monthly_30 = 0
df_price_30.to_csv(f"../data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
#turnover
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics.loc["BTC", "monthly_turnover"] = 0
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
