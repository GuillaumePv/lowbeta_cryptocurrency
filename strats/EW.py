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

import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))

import config as c
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#create weights
df_weights = df_returns.applymap(lambda x: 1/c.number_cryptos)

#returns
df_returns_EW = df_returns * df_weights

#portfolio
df_perf = df_returns_EW.sum(axis=1)
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100

df_price.to_csv(f"../data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
