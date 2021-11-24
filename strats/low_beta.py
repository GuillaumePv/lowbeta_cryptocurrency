print(40*"=")
print("Low_Beta strat")
print(40*"=")

import pandas as pd
pd.set_option('display.max_rows', 2000)
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
from tqdm import tqdm

import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_returns_CW = pd.read_csv(f"../data/processed/CW_perf_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#beta calc
df_returns['CW'] = df_returns_CW.iloc[:, 0] #add the market cap weighted returns
df_beta = pd.DataFrame(index=df_returns.index, columns=df_returns.columns)

for i, idx in enumerate(df_returns.index):
    if i > 0:
        cov = df_returns.loc[:idx, :].cov()
        df_beta.loc[idx] = cov.iloc[:, -1].values / np.diag(cov)



#Weights
df_beta_adj = df_beta.iloc[1:, :-1].copy() #remove the CW portfolio
df_weights_low = df_beta_adj.copy()
df_weights_high = df_beta_adj.copy()

if c.number_cryptos > 20:
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

else:
    avg = pd.Series(df_beta_adj.median(axis=1), index = df_beta_adj.index)

    for i in tqdm(df_beta_adj.index):
        df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: 2/(c.number_cryptos) if x <= avg.loc[i] else 0)
        df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: 2/(c.number_cryptos) if x > avg.loc[i] else 0)

#print(df_weights_low.head(1).iloc[:, :6])
#print(df_weights_high.head(1).iloc[:, :6])

#portfolio
##########
df_returns_adjusted = df_returns.iloc[1:, ].copy()
df_returns_low = df_weights_low * df_returns_adjusted
df_returns_high = df_weights_high * df_returns_adjusted

df_perf_low = df_returns_low.sum(axis=1)
df_perf_low[0] = 0
df_price_low = df_perf_low.add(1).cumprod()*100
#print(df_price_low.tail(3))
df_price_low.to_csv(f"../data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

df_perf_high = df_returns_high.sum(axis=1)
df_perf_high[0] = 0
df_price_high = df_perf_high.add(1).cumprod()*100
#print(df_price_high.tail(3))
df_price_high.to_csv(f"../data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#turnover rate
df_metrics = pd.read_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
turnover_monthly = getMonthlyTurnover(df_weights_low)
df_metrics.loc["Low Beta", "monthly_turnover"] = turnover_monthly
turnover_monthly = getMonthlyTurnover(df_weights_high)
df_metrics.loc["High Beta", "monthly_turnover"] = turnover_monthly
#print(df_metrics)
df_metrics.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#rebalance 7 days
results_7 = createPortfolio7(df_weights_low, df_returns)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["Low Beta", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"../data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

results_7 = createPortfolio7(df_weights_high, df_returns)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["High Beta", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"../data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights_low, df_returns)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["Low Beta", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"../data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")

results_30 = createPortfolio30(df_weights_high, df_returns)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["High Beta", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"../data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"../data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
