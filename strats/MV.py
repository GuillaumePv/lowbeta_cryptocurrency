print(40*"=")
print("Min Var strat")
print(40*"=")

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from tqdm import tqdm

import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
from scipy.optimize import minimize
import config as c
marketcap = format(c.market_cap,'.0e')

#min variance opti
def Min_variance(alloc, return_cov_matrix):
    matrix_one = np.ones(len(return_cov_matrix))
    criterion = 0.5*np.dot(np.transpose(alloc).dot(return_cov_matrix),alloc)
    return criterion

def optimizer(cov_matrix_test):
    length = len(cov_matrix_test)

    x0 = np.zeros(length) + 0.001

    Bounds= [(0 , 1) for i in range(0,length)] #Long only positions
    cons=({'type':'eq', 'fun': lambda x:sum(x)-1}) #Sum of weights is equal to 1


    #Optimisation
    res_MIN_VAR = minimize(Min_variance, x0, method='SLSQP', args=(cov_matrix_test),bounds=Bounds,constraints=cons,options={'disp': False})
    return res_MIN_VAR.x

#returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)
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
df_price.to_csv(f"../data/strats/MV_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
