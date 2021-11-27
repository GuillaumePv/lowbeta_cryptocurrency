print(40*"=")
print("EW strat")
print(40*"=")
import pandas as pd
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
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#create weights
df_weights = df_returns.applymap(lambda x: 1/c.number_cryptos)

#returns
df_returns_EW = df_returns * df_weights

#portfolio
df_perf = df_returns_EW.sum(axis=1)
df_perf.to_csv(f"{path_data_processed}/EW_perf_{c.number_cryptos}_1e{marketcap[-1]}.csv") #for the low beta calc
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100

df_price.to_csv(f"{path_data_processed}/EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#turnover rate
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
turnover_monthly = getMonthlyTurnover(df_weights)
df_metrics.loc["EW", "monthly_turnover"] = turnover_monthly
#print(df_metrics)
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#rebalance 7 days
results_7 = createPortfolio7(df_weights, df_returns)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["EW", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"{path_data_strat}/EW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights, df_returns)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["EW", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"{path_data_strat}/EW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
