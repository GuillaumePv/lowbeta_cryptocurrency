import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

def getPrice(df_weights, df_returns):
    df_returns_weighted = df_returns * df_weights
    df_perf = df_returns_weighted.sum(axis=1)
    df_perf[0] = 0
    df_price = df_perf.add(1).cumprod()*100
    return df_price

def getMonthlyTurnover(df_weights):
    df_turnover = df_weights - df_weights.shift(1)
    df_turnover = df_turnover.fillna(0).abs()
    df_turnover = df_turnover.sum(axis=1)
    df_turnover.replace([np.inf, -np.inf], np.nan, inplace=True)
    turnover = df_turnover.sum()

    number_of_months = int((pd.to_datetime(df_weights.index[-1]) - pd.to_datetime(df_weights.index[0]))/np.timedelta64(1,'M'))
    return turnover/number_of_months

def createPortfolio7(df_weights, df_returns):
    idx = df_weights.index
    initial_len = len(df_weights)
    seven_multiple = range(0, initial_len, 7)
    #remove all thats not seven multiple
    df_weights = df_weights.iloc[seven_multiple]
    #copy 7 times each row
    df_weights = df_weights.loc[df_weights.index.repeat(7)]
    df_weights = df_weights.iloc[:initial_len]
    #reuse initial index
    df_weights.set_index(idx, inplace=True)
    #create the portfolio price
    df_price = getPrice(df_weights, df_returns)
    #turnover
    turnover = getMonthlyTurnover(df_weights)
    return (df_price, turnover)


def createPortfolio30(df_weights, df_returns):
    idx = df_weights.index
    initial_len = len(df_weights)
    thirty_multiple = range(0, initial_len, 30)
    #remove all thats not seven multiple
    df_weights = df_weights.iloc[thirty_multiple]
    #copy 7 times each row
    df_weights = df_weights.loc[df_weights.index.repeat(30)]
    df_weights = df_weights.iloc[:initial_len]
    #reuse initial index
    df_weights.set_index(idx, inplace=True)
    #create the portfolio price
    df_price = getPrice(df_weights, df_returns)
    #turnover
    turnover = getMonthlyTurnover(df_weights)
    return (df_price, turnover)
