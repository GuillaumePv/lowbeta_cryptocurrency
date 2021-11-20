import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

def getMonthlyTurnover(df_weights):
    df_turnover = df_weights - df_weights.shift(1)
    df_turnover = df_turnover.fillna(0).abs()
    df_turnover = df_turnover.sum(axis=1)
    df_turnover.replace([np.inf, -np.inf], np.nan, inplace=True)
    turnover = df_turnover.sum()

    number_of_months = int((pd.to_datetime(df_weights.index[-1]) - pd.to_datetime(df_weights.index[0]))/np.timedelta64(1,'M'))
    return turnover/number_of_months
