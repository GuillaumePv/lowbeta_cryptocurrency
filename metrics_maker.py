############################################################################
#This file is used to create metrics tables with price data of portfolios
#it uses the cap-weighted as a market portfolio
############################################################################

#utilities
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_data

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
    columns=['monthly_returns', 'vol_roll_120', 'sharpe', 'excReturns', 'beta', 'TE', 'IR', 'OWTurnover', 'max_drawdown', 'hit_ratio'],
    index=['CW', 'EW'])

#if REBALANCING_TIME == 'daily':
for idx_metric,df in enumerate(df_list):
    df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    #Rolling Volatility
    df['rol_vol_120'] = df.pct_change().rolling(120).std()
    df.dropna(inplace=True)
    df_metrics.iloc[idx_metric, 1] = df['rol_vol_120'].mean()

    #Total return
    first_date = df.index[0] + relativedelta(day=31)
    df = df.loc[first_date:]
    number_of_months = int((df.index[-1] - first_date)/np.timedelta64(1,'M'))
    last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
    df_month = df.loc[last_day_months, :]
    df_month['returns'] = (df_month.iloc[:, 0] - df_month.iloc[:, 0].shift())/df.iloc[:, 0]
    df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
    if idx_metric != 0:
        df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]

    #sharpe
    last_date=df.index[-1].strftime("%Y-%m-%d")
    rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    if rf == 0: #if rf is not available
        last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
    rf_monthly = pow(rf/100 + 1, 1/12) - 1
    df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

print(df_metrics)

#Excess returns over benchmark

#Tracking error

#Information ratio

#One-Way Turnover


#Then some factor analysis
##########################

#Size

#Low-Volatility

#Dividends
