#program message
print(40*"=")
print("Low_Vol strat")
print(40*"=")

#utilities
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta
from pathlib import Path
pd.set_option('display.max_rows', 2000)

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

#adding directory to path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

#set up env variables + helper functions
import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30, getHerfindahl
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#get_vol
df_vol = df_returns.rolling(c.windows).std().fillna(0)[c.windows:]

#weights
df_weights_low = df_vol.copy()
df_weights_high = df_vol.copy()

if c.number_cryptos > 20: #use first and last quintile if >20
    #low weights
    df_weights_low = df_weights_low.apply(lambda x: pd.qcut(x, 5, labels=False), axis=1)
    for i in range(1,5):
        df_weights_low.replace({i:10}, inplace=True)
    df_weights_low.replace({0:1}, inplace=True)
    df_weights_low.replace({10:0}, inplace=True)
    df_weights_low['sum'] = df_weights_low.sum(axis=1)
    for col in df_weights_low.iloc[:, :-1].columns:
        df_weights_low[col] = df_weights_low[col]/df_weights_low['sum']
    del df_weights_low['sum']

    #high weights
    df_weights_high = df_weights_high.apply(lambda x: pd.qcut(x, 5, labels=False), axis=1)
    for i in range(1,4):
        df_weights_high.replace({i:0}, inplace=True)
    df_weights_high.replace({4:1}, inplace=True)
    df_weights_high['sum'] = df_weights_high.sum(axis=1)

    for col in df_weights_high.iloc[:, :-1].columns:
        df_weights_high[col] = df_weights_high[col]/df_weights_high['sum']
    del df_weights_high['sum']

else: #use median if <20
    avg = pd.Series(df_vol.median(axis=1), index=df_vol.index)

    for i in tqdm(df_vol.index):
        df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: 2/(c.number_cryptos) if x <= avg.loc[i] else 0)
        df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: 2/(c.number_cryptos) if x > avg.loc[i] else 0)


#performance
df_returns_adj = df_returns[c.windows:].copy()
df_returns_low = df_weights_low * df_returns_adj
df_returns_high = df_weights_high * df_returns_adj

df_perf_low = df_returns_low.sum(axis=1)
df_perf_low[0] = 0
df_price_low = df_perf_low.add(1).cumprod()*100
df_price_low.to_csv(f"{path_data_strat}/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

df_perf_high = df_returns_high.sum(axis=1)
df_perf_high[0] = 0
df_price_high = df_perf_high.add(1).cumprod()*100
df_price_high.to_csv(f"{path_data_strat}/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#turnover rate
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
turnover_monthly = getMonthlyTurnover(df_weights_low)
df_metrics.loc["Low Vol", "monthly_turnover"] = turnover_monthly
turnover_monthly = getMonthlyTurnover(df_weights_high)
df_metrics.loc["High Vol", "monthly_turnover"] = turnover_monthly
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#Herfindahl
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
herfindahl = getHerfindahl(df_weights_low)
df_metrics.loc["Low Vol", "HHI"] = herfindahl
herfindahl = getHerfindahl(df_weights_high)
df_metrics.loc["High Vol", "HHI"] = herfindahl
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")


#rebalance 7 days
results_7 = createPortfolio7(df_weights_low, df_returns_adj)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["Low Vol", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"{path_data_strat}/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

results_7 = createPortfolio7(df_weights_high, df_returns_adj)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["High Vol", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"{path_data_strat}/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights_low, df_returns_adj)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["Low Vol", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"{path_data_strat}/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")

results_30 = createPortfolio30(df_weights_high, df_returns_adj)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["High Vol", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"{path_data_strat}/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
