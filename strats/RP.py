import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from tqdm import tqdm
import plotly.express as px
import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
from scipy.optimize import minimize
import config as c
marketcap = format(c.market_cap,'.0e')

def MCR_calc(alloc, Returns):
    """
    This function computes the marginal contribution to risk (MCR), which
    determine how much the portfolio volatility would change if we increase
    the weight of a particular asset.

    Parameters
    ----------
    alloc : TYPE
        Weights in the investor's portfolio
    Returns : TYPE
        The returns of the portfolio's assets
    Returns
    -------
    MCR : Object
        Marginal contribution to risk (MCR)
    """
    ptf=np.multiply(Returns,alloc)
    ptfReturns=np.sum(ptf,1); # Summing across columns
    vol_ptf=np.std(ptfReturns)
    Sigma=np.cov(np.transpose(Returns))
    MCR=np.matmul(Sigma,np.transpose(alloc))/vol_ptf
    return MCR

###ERC Allocation###
def ERC(alloc,Returns):
    """
    This function computes the Equally-Weighted Risk Contribution Portfolio (ERC),
    which attributes the same risk contribution to all the assets.

    Parameters
    ----------
    alloc : TYPE
        Weights in the investor's portfolio
    Returns : TYPE
        The returns of the portfolio's assets
    Returns
    -------
    criterions : Object
        Optimal weights of assets in the portfolio.
    """
    ptf=np.multiply(Returns.iloc[:,:],alloc);
    ptfReturns=np.sum(ptf,1); # Summing across columns
    vol_ptf=np.std(ptfReturns);
    indiv_ERC=alloc*MCR_calc(alloc,Returns);
    criterion=np.power(indiv_ERC-vol_ptf/len(alloc),2)
    criterion=np.sum(criterion)*1000000000
    return criterion

def optimizer_ERC(ERC_df):
    length = ERC_df.shape[1]
    x0 = np.zeros(length)+0.0001 #Set the first weights of the Gradient Descent
    #x0 = np.zeros(len(df_ERC))+0.0001

    cons=({'type':'eq', 'fun': lambda x:sum(x)-1}) #Sum of weights is equal to 1

    Bounds= [(0 , 1) for i in range(0,length)] #Long only positions


    #Optimisation
    res_ERC = minimize(ERC, x0, method='SLSQP', args=(ERC_df),bounds=Bounds,constraints=cons,options={'disp': False})
    return res_ERC.x


#get returns
df_returns = pd.read_csv(f"../data/processed/returns_first_{c.number_cryptos}_1e{marketcap[-1]}.csv", index_col=0)

#get weights
weights_ERC = []
for i in tqdm(range(df_returns.shape[0])):
    cov_matrix = df_returns.iloc[i:c.windows+i]
    weight = optimizer_ERC(cov_matrix)
    weights_ERC.append(weight)

df_weights = pd.DataFrame(weights_ERC, index=df_returns.index, columns=df_returns.columns)

#portfolio
df_returns_ERC = df_weights*df_returns
df_perf = df_returns_ERC.sum(axis=1)
df_perf[0] = 0
df_price = df_perf.add(1).cumprod()*100
print(df_price)
df_price.to_csv(f"../data/strats/ERC_price_{c.number_cryptos}_1e{marketcap[-1]}.csv")
