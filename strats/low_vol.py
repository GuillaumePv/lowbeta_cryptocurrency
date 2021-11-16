print(40*"=")
print("Low_Vol strat")
print(40*"=")

import pandas as pd
pd.set_option('display.max_rows', 2000)
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
import inspect

import config as c
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#get_vol
df_vol = df_returns.rolling(c.windows).std().fillna(0)[c.windows:]

#weights
df_weights_low = df_vol.copy()
df_weights_high = df_vol.copy()

avg = pd.Series(df_vol.median(axis=1), index=df_vol.index)

for i in tqdm(df_vol.index):
    df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: 2/(c.number_cryptos) if x <= avg.loc[i] else 0)
    df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: 2/(c.number_cryptos) if x > avg.loc[i] else 0)


#print(avg[:2])
#print(df_vol.head(2).iloc[:, :10])
#print(df_weights_low.head(2).iloc[:, :10])
#print(df_weights_high.head(2).iloc[:, :10])

df_returns_low = df_weights_low * df_returns[c.windows:]
df_returns_high = df_weights_high * df_returns[c.windows:]

#portfolio
df_perf_low = df_returns_low.sum(axis=1)
df_perf_low[0] = 0
df_price_low = df_perf_low.add(1).cumprod()*100
print(df_price_low.tail(3))
df_price_low.to_csv(f"../data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

df_perf_high = df_returns_high.sum(axis=1)
df_perf_high[0] = 0
df_price_high = df_perf_high.add(1).cumprod()*100
print(df_price_high.tail(3))
df_price_high.to_csv(f"../data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
