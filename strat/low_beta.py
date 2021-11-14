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
df_beta_adj = df_beta.iloc[:, :-1].dropna().copy() #remove the CW portfolio
df_weights_low = df_beta_adj.copy()
df_weights_high = df_beta_adj.copy()


avg = pd.Series(df_beta_adj.median(axis=1), index = df_beta_adj.index)

for i in tqdm(df_beta_adj.index):
    df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: x if x <= avg.loc[i] else 0)
    df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: (x - df_weights_low.loc[i].min())/(df_weights_low.loc[i].max()-df_weights_low.loc[i].min()) if x != 0 else 0)
    df_weights_low.loc[i] = df_weights_low.loc[i]/df_weights_low.loc[i].sum()

    df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: x if x > avg.loc[i] else 0)
    df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: (x - df_weights_high.loc[i].min())/(df_weights_high.loc[i].max()-df_weights_high.loc[i].min()) if x != 0 else 0)
    df_weights_high.loc[i] = df_weights_high.loc[i]/df_weights_high.loc[i].sum()

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
print(df_price_low.tail(3))
df_price_low.to_csv(f"../data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

df_perf_high = df_returns_high.sum(axis=1)
df_perf_high[0] = 0
df_price_high = df_perf_high.add(1).cumprod()*100
print(df_price_high.tail(3))
df_price_low.to_csv(f"../data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
