############################################################################
#This file is used to create metrics tables with price data of portfolios
#it uses the cap-weighted as a market portfolio
############################################################################
#message for makefile
print(40*"=")
print("CREATING METRICS")
print(40*"=")

import math
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
import numpy as np
from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_data
from matplotlib import pyplot as plt
import config as c
marketcap = format(c.market_cap,'.0e')

#create the dataframes
CW = pd.read_csv(f"data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
EW = pd.read_csv(f"data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
MV = pd.read_csv(f"data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Vol = pd.read_csv(f"data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Vol = pd.read_csv(f"data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
#RP = pd.read_csv(f"data/strats/ERC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Beta = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Beta = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

df_list = [CW, EW, MV, Low_Vol, High_Vol, Low_Beta, High_Beta]

#print(len(CW), len(EW), len(MV), len(Low_Vol), len(High_Vol), len(Low_Beta), len(High_Beta))

#get first_date on every df
date_start = '2009-01-01'
for df in df_list:
    first_date = df.head(1).index
    first_date
    first_date = first_date[0]
    if pd.to_datetime(first_date).tz_convert(None) > pd.to_datetime(date_start).tz_localize(None):
        date_start = first_date

print("DATE START", date_start)



#create a df with all of the prices trunc
list_df = ["cap_weighted_index", "ponderated_index", "MV", "LV", "HV", "LB", "HB"]

#get df at same length & make them start at 100
df_list_adj = []
df_test =pd.DataFrame()

for i,df in enumerate(df_list):
    df = df.loc[df.index >= date_start].copy()
    df = df.pct_change()
    df.iloc[0]=0
    df = df.add(1).cumprod()*100
    df_list_adj.append(df)


    #all df creation
    if i == 0:
        df_all = pd.DataFrame(columns=list_df, index=df.index)
    print(df_test.index.difference(df.index))

    df_all[list_df[i]] = df.values
    df_test = df

df_all.to_csv(f"data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#for i in df_list_adj:
#    print(len(i))

CW = df_list_adj[0] #because of truncated

#First some simple metrics
##########################

df_metrics = pd.read_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#if rebalance == 'daily':
for idx_metric,df in enumerate(df_list_adj):
    df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    #Rolling Volatility
    df['volatility'] = df.pct_change().rolling(120).std()
    df.dropna(inplace=True)
    df_metrics.iloc[idx_metric, 1] = df['volatility'].mean() * math.sqrt(365/12)

    #Total return
    first_date = df.index[0] + relativedelta(day=31)
    df_trunc = df.loc[first_date:]
    number_of_months = int((df_trunc.index[-1] - first_date)/np.timedelta64(1,'M'))
    last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
    df_month = df_trunc.loc[last_day_months, :]
    df_month['returns'] = (df_month.iloc[:, 0] - df_month.iloc[:, 0].shift())/df_month.iloc[:, 0]
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    #Excess returns over benchmark
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
    else:
        df_metrics.iloc[idx_metric, 3] = 0

    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

    #beta
    bench_returns = CW.iloc[:, 0].pct_change()
    #print(len(CW))
    #print(len(df))
    df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
    df_cov.dropna(inplace=True)
    cov = df_cov.cov().iloc[0,1]
    beta = cov/pow(df.iloc[:, 0].pct_change().std(),2)
    df_metrics.iloc[idx_metric, 4] = beta

    #Max drawdown
    max_drawdown=min(df_month['returns'].dropna().values)
    df_metrics.iloc[idx_metric, 5] = max_drawdown

    #Tracking error
    df['returns'] = df.iloc[:, 0].pct_change()
    CW['returns'] = CW.iloc[:, 0].pct_change()
    df['excess_returns'] = df['returns'] - CW['returns']
    df_metrics.iloc[idx_metric, 6] = df['excess_returns'].std()

    #Information ratio
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 7] = df['excess_returns'].sum()/df_metrics.iloc[idx_metric, 6]

    df_metrics.to_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")
print(df_metrics)


#####################
#REBALANCE 7 METRICS
#####################

#create the dataframes
CW = pd.read_csv(f"data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
EW = pd.read_csv(f"data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
MV = pd.read_csv(f"data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Vol = pd.read_csv(f"data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Vol = pd.read_csv(f"data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
#RP = pd.read_csv(f"data/strats/ERC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Beta = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Beta = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)

df_list = [CW, EW, MV, Low_Vol, High_Vol, Low_Beta, High_Beta]

#print(len(CW), len(EW), len(MV), len(Low_Vol), len(High_Vol), len(Low_Beta), len(High_Beta))

#get first_date on every df
date_start = '2009-01-01'
for df in df_list:
    first_date = df.head(1).index
    first_date
    first_date = first_date[0]
    if pd.to_datetime(first_date).tz_convert(None) > pd.to_datetime(date_start).tz_localize(None):
        date_start = first_date

print("DATE START", date_start)



#create a df with all of the prices trunc
list_df = ["cap_weighted_index", "ponderated_index", "MV", "LV", "HV", "LB", "HB"]

#get df at same length & make them start at 100
df_list_adj = []
df_test =pd.DataFrame()

for i,df in enumerate(df_list):
    df = df.loc[df.index >= date_start].copy()
    df = df.pct_change()
    df.iloc[0]=0
    df = df.add(1).cumprod()*100
    df_list_adj.append(df)


    #all df creation
    if i == 0:
        df_all = pd.DataFrame(columns=list_df, index=df.index)
    print(df_test.index.difference(df.index))

    df_all[list_df[i]] = df.values
    df_test = df

df_all.to_csv(f"data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#for i in df_list_adj:
#    print(len(i))

CW = df_list_adj[0] #because of truncated

#First some simple metrics
##########################

df_metrics = pd.read_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)

#if rebalance == 'daily':
for idx_metric,df in enumerate(df_list_adj):
    df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    #Rolling Volatility
    df['volatility'] = df.pct_change().rolling(120).std()
    df.dropna(inplace=True)
    df_metrics.iloc[idx_metric, 1] = df['volatility'].mean() * math.sqrt(365/12)

    #Total return
    first_date = df.index[0] + relativedelta(day=31)
    df_trunc = df.loc[first_date:]
    number_of_months = int((df_trunc.index[-1] - first_date)/np.timedelta64(1,'M'))
    last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
    df_month = df_trunc.loc[last_day_months, :]
    df_month['returns'] = (df_month.iloc[:, 0] - df_month.iloc[:, 0].shift())/df_month.iloc[:, 0]
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    #Excess returns over benchmark
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
    else:
        df_metrics.iloc[idx_metric, 3] = 0

    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

    #beta
    bench_returns = CW.iloc[:, 0].pct_change()
    #print(len(CW))
    #print(len(df))
    df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
    df_cov.dropna(inplace=True)
    cov = df_cov.cov().iloc[0,1]
    beta = cov/pow(df.iloc[:, 0].pct_change().std(),2)
    df_metrics.iloc[idx_metric, 4] = beta

    #Max drawdown
    max_drawdown=min(df_month['returns'].dropna().values)
    df_metrics.iloc[idx_metric, 5] = max_drawdown

    #Tracking error
    df['returns'] = df.iloc[:, 0].pct_change()
    CW['returns'] = CW.iloc[:, 0].pct_change()
    df['excess_returns'] = df['returns'] - CW['returns']
    df_metrics.iloc[idx_metric, 6] = df['excess_returns'].std()

    #Information ratio
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 7] = df['excess_returns'].sum()/df_metrics.iloc[idx_metric, 6]

    df_metrics.to_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
print(df_metrics)
