############################################################################
#This file is used to create metrics tables with price data of portfolios
#it uses the cap-weighted as a market portfolio
############################################################################

#utilities
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

#environment vars
NUMBER_OF_CRYPTOS = 20
REBALANCING_TIME = 'daily' #can be either daily, monthly, quarterly

#create the dataframes
CW = pd.read_csv(f"data/processed/CW_{NUMBER_OF_CRYPTOS}_price.csv", index_col=0)
EW = pd.read_csv(f"data/processed/EW_{NUMBER_OF_CRYPTOS}_price.csv", index_col=0)

df_list = [CW, EW]

#First some simple metrics
##########################

df_metrics = pd.DataFrame(
    columns=['monthly_returns', 'vol', 'sharpe', 'excReturns', 'beta', 'TE', 'IR', 'OWTurnover', 'max_drawdown', 'hit_ratio'],
    index=['CW', 'EW'])

#if REBALANCING_TIME == 'daily':
#Total return
for idx_metric,df in enumerate(df_list):
    df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    first_date = df.index[0] + relativedelta(day=31)
    df = df.loc[first_date:]
    number_of_months = int((df.index[-1] - first_date)/np.timedelta64(1,'M'))
    last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
    df = df.loc[last_day_months, :]
    df['returns'] = (df.iloc[:, 0] - df.iloc[:, 0].shift(1))/df.iloc[:, 0]
    df_metrics.iloc[idx_metric, 0] = df['returns'].mean()
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]

print(df_metrics)

#Volatility

#Sharpe ratio

#Excess returns over benchmark

#Tracking error

#Information ratio

#One-Way Turnover


#Then some factor analysis
##########################

#Size

#Low-Volatility

#Dividends
