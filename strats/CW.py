#message for program
print(40*"=")
print("STARTING STRATS")
print(40*"=")

print(40*"=")
print("CW strat")
print(40*"=")

#utilities
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
import sys
from datetime import datetime
from datetime import timedelta
from matplotlib import style
from pathlib import Path
style.use('fivethirtyeight')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

# adding directory to path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# set up env variables + helper functions
import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30, getHerfindahl
marketcap = format(c.market_cap,'.0e')


#get first_date
df_market_cap = pd.read_csv(f'{path_data_processed}/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv', index_col=0)
df_market_cap_first = df_market_cap.iloc[:c.number_cryptos]
first_date = df_market_cap_first['first_date_marketcap'].tail(1).values
first_date = first_date[0]

#get marketcaps
df_marketcap = pd.read_csv(f'{path_data_processed}/market_cap_crypto.csv', index_col=0)
df_marketcap = df_marketcap.loc[df_marketcap.index > first_date]
df_marketcap = df_marketcap.loc[:, df_market_cap_first['crypto_name']]
df_marketcap['sum'] = df_marketcap.sum(axis=1)

#weigths
df_weights = pd.DataFrame(index=df_marketcap.index, columns=df_marketcap.iloc[:, :-1].columns)
for col in df_marketcap.iloc[:, :-1].columns:
    df_weights.loc[:, col] = df_marketcap.loc[:, col]/df_marketcap['sum']
df_weights=df_weights.iloc[1:]


#returns
df_returns = pd.read_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_returns_CW = df_returns * df_weights
df_weights.to_csv(f"{path_data_processed}/CW_weights_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#portfolio
df_perf = df_returns_CW.sum(axis=1)
df_perf.to_csv(f"{path_data_processed}/CW_perf_{c.number_cryptos}_1e{marketcap[-1]}.csv") #for the low beta calc
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100
df_price.to_csv(f"{path_data_strat}/CW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#turnover rate
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
turnover_monthly = getMonthlyTurnover(df_weights)
df_metrics.loc["CW", "monthly_turnover"] = turnover_monthly
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#Herfindahl
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
herfindahl = getHerfindahl(df_weights)
df_metrics.loc["CW", "HHI"] = herfindahl
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#rebalance 7 days
results_7 = createPortfolio7(df_weights, df_returns)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["CW", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"{path_data_strat}/CW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights, df_returns)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["CW", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"{path_data_strat}/CW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
