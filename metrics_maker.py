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

print("=== Computing metrics rebalancing each day ===")
#create the dataframes
CW = pd.read_csv(f"data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
BTC = pd.read_csv(f"data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
EW = pd.read_csv(f"data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
MV = pd.read_csv(f"data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Vol = pd.read_csv(f"data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Vol = pd.read_csv(f"data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Beta = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Beta = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Beta_EW = pd.read_csv(f"data/strats/Low_Beta_EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Beta_EW = pd.read_csv(f"data/strats/High_Beta_EW_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
Low_Beta_BTC = pd.read_csv(f"data/strats/Low_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
High_Beta_BTC = pd.read_csv(f"data/strats/High_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
print(len(MV))
print(len(Low_Vol))
df_list = [CW, BTC, EW, MV, Low_Vol, High_Vol, Low_Beta, High_Beta, Low_Beta_EW, High_Beta_EW, Low_Beta_BTC, High_Beta_BTC]

#print(len(CW), len(EW), len(MV), len(Low_Vol), len(High_Vol), len(Low_Beta), len(High_Beta))

#get first_date on every df
date_start = '2009-01-01'
for df in df_list:
    first_date = df.head(1).index
    first_date = first_date[0]
    if pd.to_datetime(first_date).tz_convert(None) > pd.to_datetime(date_start).tz_localize(None):
        date_start = first_date


print("DATE START", date_start)



#create a df with all of the prices trunc
list_df = ["cap_weighted_index", "BTC", "ponderated_index", "MV", "LV", "HV", "LB", "HB", "LB_EW", "HB_EW", "LB_BTC", "HB_BTC"]

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
    if len(df_test.index.difference(df.index)):
        print(df_test.index.difference(df.index))

    df_all[list_df[i]] = df.values
    df_test = df

df_all.to_csv(f"data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
#print(df_all)

#for i in df_list_adj:
#    print(len(i))

# Choose your benchmark
CW = df_list_adj[0]
BTC = df_list_adj[1]
EW = df_list_adj[2] #because of truncated

# process benchmark in order to create a t-stat
df_CW = CW
df_CW.index = pd.to_datetime(df_CW.index,format='%Y-%m-%d')
df_CW.dropna(inplace=True)
first_date = df_CW.index[0] + relativedelta(day=31)
df_trunc_CW = df_CW.loc[first_date:]
number_of_months = int((df_trunc_CW.index[-1] - first_date)/np.timedelta64(1,'M'))
last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
df_month_CW = df_trunc_CW.loc[last_day_months, :]
df_month_CW['returns'] = df_month_CW.iloc[:, 0].pct_change()

#First some simple metrics
##########################

df_metrics = pd.read_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
# print(df_list_adj)
#if rebalance == 'daily':
array_t_stat = []
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
    df_month['returns'] = df_month.iloc[:, 0].pct_change()
    df_month['Excess_return_monthly'] = df_month['returns'] - df_month_CW['returns']
    # print(list_df[idx_metric])
    std = np.std(df_month['Excess_return_monthly'])
    mean = np.mean(df_month['Excess_return_monthly'])
    number_observation = len(df_month['Excess_return_monthly'])
    # print("std of excess return: ", std)
    # print("mean of excess return: ", mean)
    # print("Number of observation: ", number_observation)
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    #df_month['return'] => monthly return for each strat
    # print(df_month['returns'])
    #Excess returns over benchmark
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
        # computing t-stat: https://www.ifa.com/articles/calculations_for_t_statistics/
        t_stat = (mean*np.sqrt(number_observation))/std
        # print('t-stat: ', t_stat)
        array_t_stat.append(t_stat)
    else:
        df_metrics.iloc[idx_metric, 3] = 0
        array_t_stat.append("None")
    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

    #beta
    if idx_metric < 8:
        bench_returns = CW.iloc[:, 0].pct_change()
    elif idx_metric < 10:
        bench_returns = EW.iloc[:, 0].pct_change()
    elif idx_metric < 12:
        bench_returns = BTC.iloc[:, 0].pct_change()

    #print(len(bench_returns))
    #print(len(df))
    df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
    df_cov.dropna(inplace=True)
    cov_matrix = df_cov.cov()
    cov = cov_matrix.iloc[0,1]
    var = cov_matrix.iloc[0,0]
    beta = cov/var
    #print("---")
    #print(idx_metric)
    #print(df_cov.cov())
    #print(cov)
    #print(pow(bench_returns.std(),2))
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

df_tstat = pd.DataFrame([array_t_stat], columns=list_df)
print(df_tstat)
print(df_metrics)
df_metrics.to_latex(f"latex/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.tex", caption=f"Metrics for each strategy with {c.number_cryptos} cryptocurrencies", label=f"metrics{c.number_cryptos}", float_format="%.2f" )

#####################
#REBALANCE 7 METRICS
#####################

print("==== Computing metrics for rebalancing 7 days ====")
#create the dataframes
CW = pd.read_csv(f"data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
BTC = pd.read_csv(f"data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
EW = pd.read_csv(f"data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
MV = pd.read_csv(f"data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Vol = pd.read_csv(f"data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Vol = pd.read_csv(f"data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
#RP = pd.read_csv(f"data/strats/ERC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Beta = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Beta = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Beta_EW = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Beta_EW = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
Low_Beta_BTC = pd.read_csv(f"data/strats/Low_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
High_Beta_BTC = pd.read_csv(f"data/strats/High_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)

df_list = [CW,BTC, EW, MV, Low_Vol, High_Vol, Low_Beta, High_Beta, Low_Beta_EW, High_Beta_EW, Low_Beta_BTC, High_Beta_BTC]

#print(len(CW), len(EW), len(MV), len(Low_Vol), len(High_Vol), len(Low_Beta), len(High_Beta))

#get first_date on every df
date_start = '2009-01-01'
for df in df_list:
    first_date = df.head(1).index
    first_date = first_date[0]
    if pd.to_datetime(first_date).tz_convert(None) > pd.to_datetime(date_start).tz_localize(None):
        date_start = first_date

print("DATE START", date_start)



#create a df with all of the prices trunc
list_df = ["cap_weighted_index", "BTC", "ponderated_index", "MV", "LV", "HV", "LB", "HB", "LB_EW", "HB_EW", "LB_BTC", "HB_BTC"]

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
    if len(df_test.index.difference(df.index)):
        print(df_test.index.difference(df.index))

    df_all[list_df[i]] = df.values
    df_test = df

df_all.to_csv(f"data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#for i in df_list_adj:
#    print(len(i))

CW = df_list_adj[0]
BTC = df_list_adj[1]
EW = df_list_adj[2] #because of truncated

# process benchmark in order to create a t-stat
df_CW = CW
df_CW.index = pd.to_datetime(df_CW.index,format='%Y-%m-%d')
df_CW.dropna(inplace=True)
first_date = df_CW.index[0] + relativedelta(day=31)
df_trunc_CW = df_CW.loc[first_date:]
number_of_months = int((df_trunc_CW.index[-1] - first_date)/np.timedelta64(1,'M'))
last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
df_month_CW = df_trunc_CW.loc[last_day_months, :]
df_month_CW['returns'] = df_month_CW.iloc[:, 0].pct_change()

#First some simple metrics
##########################

df_metrics = pd.read_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
array_t_stat = []
#if rebalance == 'daily':

for idx_metric,df in enumerate(df_list_adj):
    df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    #Rolling Volatility
    df['volatility'] = df.pct_change().rolling(120).std()
    df.dropna(inplace=True)
    # monthly volatility
    df_metrics.iloc[idx_metric, 1] = df['volatility'].mean() * math.sqrt(365/12)

    #Total return
    first_date = df.index[0] + relativedelta(day=31)
    df_trunc = df.loc[first_date:]
    number_of_months = int((df_trunc.index[-1] - first_date)/np.timedelta64(1,'M'))
    last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
    df_month = df_trunc.loc[last_day_months, :]
    df_month['returns'] = df_month.iloc[:, 0].pct_change()
    df_month['Excess_return_monthly'] = df_month['returns'] - df_month_CW['returns']

    std = np.std(df_month['Excess_return_monthly'])
    mean = np.mean(df_month['Excess_return_monthly'])
    number_observation = len(df_month['Excess_return_monthly'])
    # print("std of excess return: ", std)
    # print("mean of excess return: ", mean)
    # print("number of observation: ", number_observation)
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    #Excess returns over benchmark
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
        t_stat = (mean*np.sqrt(number_observation))/std
        # print('t-stat: ', t_stat)
        array_t_stat.append(t_stat)
    else:
        df_metrics.iloc[idx_metric, 3] = 0
        array_t_stat.append("None")

    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

    #beta
    if idx_metric < 8:
        bench_returns = CW.iloc[:, 0].pct_change()
    elif idx_metric < 10:
        bench_returns = EW.iloc[:, 0].pct_change()
    elif idx_metric < 12:
        bench_returns = BTC.iloc[:, 0].pct_change()

    df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
    df_cov.dropna(inplace=True)
    cov_matrix = df_cov.cov()
    cov = cov_matrix.iloc[0,1]
    var = cov_matrix.iloc[0,0]
    beta = cov/var
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
print("REB 7")
df_tstat = pd.DataFrame([array_t_stat], columns=list_df)
print(df_tstat)
print(df_metrics)
df_metrics.to_latex(f"latex/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.tex", caption=f"Metrics for each strategy with {c.number_cryptos} cryptocurrencies (Rebalanced 7 days)", label=f"metrics{c.number_cryptos}_7", float_format="%.2f" )
#####################
#REBALANCE 30 METRICS
#####################

print("=== Computing Rebalancing 30 days ===")
#create the dataframes
CW = pd.read_csv(f"data/strats/CW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
BTC = pd.read_csv(f"data/strats/BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
EW = pd.read_csv(f"data/strats/EW_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
MV = pd.read_csv(f"data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
Low_Vol = pd.read_csv(f"data/strats/Low_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
High_Vol = pd.read_csv(f"data/strats/High_Vol_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
#RP = pd.read_csv(f"data/strats/ERC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
Low_Beta = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
High_Beta = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
Low_Beta_EW = pd.read_csv(f"data/strats/Low_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
High_Beta_EW = pd.read_csv(f"data/strats/High_Beta_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
Low_Beta_BTC = pd.read_csv(f"data/strats/Low_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
High_Beta_BTC = pd.read_csv(f"data/strats/High_Beta_BTC_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
print(len(MV))
print(len(Low_Vol))
df_list = [CW, BTC, EW, MV, Low_Vol, High_Vol, Low_Beta, High_Beta, Low_Beta_EW, High_Beta_EW, Low_Beta_BTC, High_Beta_BTC]

#print(len(CW), len(EW), len(MV), len(Low_Vol), len(High_Vol), len(Low_Beta), len(High_Beta))

#get first_date on every df
date_start = '2009-01-01'

for df in df_list:
    first_date = df.head(1).index
    first_date = first_date[0]
    if pd.to_datetime(first_date).tz_convert(None) > pd.to_datetime(date_start).tz_localize(None):
        date_start = first_date

print("DATE START", date_start)



#create a df with all of the prices trunc
list_df = ["cap_weighted_index", "BTC", "ponderated_index", "MV", "LV", "HV", "LB", "HB", "LB_EW", "HB_EW", "LB_BTC", "HB_BTC"]

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
    if len(df_test.index.difference(df.index)):
        print(df_test.index.difference(df.index))

    df_all[list_df[i]] = df.values
    df_test = df

df_all.to_csv(f"data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")

#for i in df_list_adj:
#    print(len(i))

CW = df_list_adj[0]
BTC = df_list_adj[1] #because of truncated
EW = df_list_adj[2]

# process benchmark in order to create a t-stat
df_CW = CW
df_CW.index = pd.to_datetime(df_CW.index,format='%Y-%m-%d')
df_CW.dropna(inplace=True)
first_date = df_CW.index[0] + relativedelta(day=31)
df_trunc_CW = df_CW.loc[first_date:]
number_of_months = int((df_trunc_CW.index[-1] - first_date)/np.timedelta64(1,'M'))
last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
df_month_CW = df_trunc_CW.loc[last_day_months, :]
df_month_CW['returns'] = df_month_CW.iloc[:, 0].pct_change()

#First some simple metrics
##########################

df_metrics = pd.read_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
array_t_stat = []
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
    df_month['returns'] = df_month.iloc[:, 0].pct_change()
    df_month['Excess_return_monthly'] = df_month['returns'] - df_month_CW['returns']

    std = np.std(df_month['Excess_return_monthly'])
    mean = np.mean(df_month['Excess_return_monthly'])
    number_observation = len(df_month['Excess_return_monthly'])
    # print("std of excess return: ", std)
    # print("mean of excess return: ", mean)
    # print("number of observation: ", number_observation)
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    #Excess returns over benchmark
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
        t_stat = (mean*np.sqrt(number_observation))/std
        # print('t-stat: ', t_stat)
        array_t_stat.append(t_stat)
    else:
        df_metrics.iloc[idx_metric, 3] = 0
        array_t_stat.append("None")

    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]
    print
    #beta
    if idx_metric < 8:
        bench_returns = CW.iloc[:, 0].pct_change()
    elif idx_metric < 10:
        bench_returns = EW.iloc[:, 0].pct_change()
    elif idx_metric < 12:
        bench_returns = BTC.iloc[:, 0].pct_change()

    #print(len(CW))
    #print(len(df))
    df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
    df_cov.dropna(inplace=True)
    cov_matrix = df_cov.cov()
    cov = cov_matrix.iloc[0,1]
    var = cov_matrix.iloc[0,0]
    beta = cov/var
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

    df_metrics.to_csv(f"data/processed/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
print("REB 30")
df_tstat = pd.DataFrame([array_t_stat], columns=list_df)
print(df_tstat)
print(df_metrics)
df_metrics.to_latex(f"latex/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.tex", caption=f"Metrics for each strategy with {c.number_cryptos} cryptocurrencies (Rebalanced 30 days)", label=f"metrics{c.number_cryptos}_30", float_format="%.2f" )
