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

pd.read_csv(f'../data/processed/crypto_date_marketcap_sorted.csv', index_col=0)
df_market_cap_first_20 = df_market_cap.iloc[:number_crypto]
