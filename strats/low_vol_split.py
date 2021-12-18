print(40*"=")
print("Low_Vol strat")
print(40*"=")

import pandas as pd
pd.set_option('display.max_rows', 2000)
from datetime import datetime
from datetime import timedelta
import numpy as np
from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_data
import matplotlib.pyplot as plt
import math

from tqdm import tqdm

from pathlib import Path

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()
path_latex = (path_original / "../latex/").resolve()


import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

import sys
sys.path.append(parentdir)

import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30, getHerfindahl
marketcap = format(c.market_cap,'.0e')

cut_date = "2019-02-01"

#get returns
df_returns = pd.read_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_returns_before = df_returns.loc[df_returns.index <= cut_date].copy()
df_returns_after = df_returns.loc[df_returns.index > cut_date].copy()

df_CW = pd.read_csv(f"{path_data_strat}/CW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
df_CW_before = df_CW.loc[df_returns_before.index]
df_CW_after = df_CW.loc[df_returns_after.index]

df = [df_returns_before, df_returns_after]

#create a metrics df
df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'volatility', 'sharpe', 'excess_returns'],
    index=['Low Vol Before', 'High Vol Before','Low Vol After', 'High Vol After' ])

views = 0
#significance for sharpe
array_sign_stat = []

for df_returns in df:
    #get_vol
    df_vol = df_returns.rolling(c.windows).std().fillna(0)[c.windows:]

    #weights
    df_weights_low = df_vol.copy()
    df_weights_high = df_vol.copy()

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
        avg = pd.Series(df_vol.median(axis=1), index=df_vol.index)

        for i in tqdm(df_vol.index):
            df_weights_low.loc[i] = df_weights_low.loc[i].apply(lambda x: 2/(c.number_cryptos) if x <= avg.loc[i] else 0)
            df_weights_high.loc[i] = df_weights_high.loc[i].apply(lambda x: 2/(c.number_cryptos) if x > avg.loc[i] else 0)


    df_returns_low = df_weights_low * df_returns[c.windows:]
    df_returns_high = df_weights_high * df_returns[c.windows:]

    #portfolio
    df_perf_low = df_returns_low.sum(axis=1)
    df_perf_low[0] = 0
    df_price_low = df_perf_low.add(1).cumprod()*100

    df_perf_high = df_returns_high.sum(axis=1)
    df_perf_high[0] = 0
    df_price_high = df_perf_high.add(1).cumprod()*100

    #turnover rate
    turnover_monthly_low = getMonthlyTurnover(df_weights_low)
    turnover_monthly_high = getMonthlyTurnover(df_weights_high)

    for df in [df_price_low, df_price_high]:
        df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
        #Rolling Volatility
        vola = df.pct_change().rolling(120).std()
        df = pd.DataFrame({'price':df, 'volatility':vola})
        #print(df)
        df.dropna(inplace=True)
        df_metrics.iloc[views, 1] = df['volatility'].mean() * math.sqrt(365/12)

        #Total return
        #print(df_CW_before.head(3))
        #print(df.head(3))
        def monthly_returns(df):
            df.set_index(pd.to_datetime(df.index), inplace=True)
            first_date = df.index[0] + relativedelta(day=31)
            df_trunc = df.loc[first_date:]
            number_of_months = int((df_trunc.index[-1] - first_date)/np.timedelta64(1,'M'))
            last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
            df_month = df_trunc.loc[last_day_months, :]
            df_month['returns'] = df_month.iloc[:, 0].pct_change()
            return df_month['returns'].mean()

        df_metrics.iloc[views, 0] = monthly_returns(df)

        #excess_returns
        if views < 2:
            bench_returns = monthly_returns(df_CW_before)
            #print(bench_returns)
            df_metrics.iloc[views, 3] = df_metrics.iloc[views, 0] - bench_returns
            number_observation=len(df_CW_before)
        else:
            bench_returns = monthly_returns(df_CW_after)
            #print(bench_returns)
            df_metrics.iloc[views, 3] = df_metrics.iloc[views, 0] - bench_returns
            number_observation=len(df_CW_after) #for significance

        #sharpe
        last_date=df.index[-1].strftime("%Y-%m-%d")
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
        if rf == 0: #if rf is not available
            last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
            rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
        rf_monthly = pow(rf/100 + 1, 1/12) - 1
        df_metrics.iloc[views, 2] = (df_metrics.iloc[views, 0] - rf_monthly)/df_metrics.iloc[views, 1]
        #check significance
        sharpe=df_metrics.iloc[views, 2]
        if sharpe > 0:
            conf = sharpe - 1.96*np.sqrt((1+0.5*sharpe)/number_observation)
            array_sign_stat.append(conf)
        else:
            conf = sharpe + 1.96*np.sqrt((1+0.5*sharpe)/number_observation)
            array_sign_stat.append(conf)

        views += 1

print(df_metrics)
print(array_sign_stat)
df_signif = pd.DataFrame([array_sign_stat], columns=df_metrics.index)
print(df_signif)
df_signif.to_csv(f"{path_data_processed}/df_low_vol_split_SIGNIFICANCE_{c.number_cryptos}_1e{marketcap[-1]}.csv")
df_metrics.to_csv(f"{path_data_processed}/df_low_vol_split_{c.number_cryptos}_1e{marketcap[-1]}.csv")
df_metrics.to_latex(f"{path_latex}/metrics_low_vol_split_{c.number_cryptos}_1e{marketcap[-1]}.tex", caption="Low volatility metrics based on split on 2019-02-01", label="low_vol_split")
