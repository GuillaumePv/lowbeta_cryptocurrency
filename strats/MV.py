#program message
print(40*"=")
print("Min Var strat")
print(40*"=")

#utlities
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
from pathlib import Path
from scipy.optimize import minimize
from matplotlib import style
style.use('fivethirtyeight')


## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

# adding directory to path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# set up env variables + helper functions
import config as c
from functions import getMonthlyTurnover, createPortfolio7, createPortfolio30, getHerfindahl
marketcap = format(c.market_cap,'.0e')

#min variance optimization functions
def Min_variance(alloc, return_cov_matrix):
    matrix_one = np.ones(len(return_cov_matrix))
    criterion = 0.5*np.dot(np.transpose(alloc).dot(return_cov_matrix),alloc)
    return criterion

def optimizer(cov_matrix_test):
    length = len(cov_matrix_test)
    x0 = np.zeros(length) + 0.001
    Bounds= [(0 , 1) for i in range(0,length)] #Long only positions
    cons=({'type':'eq', 'fun': lambda x:sum(x)-1}) #Sum of weights is equal to 1

    res_MIN_VAR = minimize(Min_variance, x0, method='SLSQP', args=(cov_matrix_test),bounds=Bounds,constraints=cons,options={'disp': False})
    return res_MIN_VAR.x

#returns
df_returns = pd.read_csv(f"{path_data_processed}/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
length_index = df_returns.shape[0]

#weights
weights_min_var = []
for i in tqdm(range(length_index-c.windows)):
    cov_matrix = df_returns.iloc[i:c.windows+i].cov()
    weight = optimizer(cov_matrix.values)
    weights_min_var.append(weight)


df_returns_adj = df_returns.iloc[c.windows:].copy()
df_weights = pd.DataFrame(weights_min_var, columns=df_returns_adj.columns, index=df_returns_adj.index)

#portfolio
df_returns_MV = df_weights*df_returns_adj
df_perf = df_returns_MV.sum(axis=1)
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100
df_price.to_csv(f"{path_data_strat}/MV_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#turnover rate
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
turnover_monthly = getMonthlyTurnover(df_weights)
df_metrics.loc["MV", "monthly_turnover"] = turnover_monthly
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#Herfindahl
df_metrics = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
herfindahl = getHerfindahl(df_weights)
df_metrics.loc["MV", "HHI"] = herfindahl
df_metrics.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}.csv")

#rebalance 7 days
results_7 = createPortfolio7(df_weights, df_returns_adj)
df_price_7 = results_7[0]
turnover_monthly_7 = results_7[1]
df_metrics_7 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv", index_col=0)
df_metrics_7.loc["MV", "monthly_turnover"] = turnover_monthly_7
df_metrics_7.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")
df_price_7.to_csv(f"{path_data_strat}/MV_price_{c.number_cryptos}_1e{marketcap[-1]}_reb7.csv")

#rebalance 30 days
results_30 = createPortfolio30(df_weights, df_returns_adj)
df_price_30 = results_30[0]
turnover_monthly_30 = results_30[1]
df_metrics_30 = pd.read_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv", index_col=0)
df_metrics_30.loc["MV", "monthly_turnover"] = turnover_monthly_30
df_metrics_30.to_csv(f"{path_data_processed}/df_metrics_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
df_price_30.to_csv(f"{path_data_strat}/MV_price_{c.number_cryptos}_1e{marketcap[-1]}_reb30.csv")
