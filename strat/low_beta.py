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

import config as c
marketcap = format(c.market_cap,'.0e')

#get returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#beta calc
