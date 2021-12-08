import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
path_original = Path(__file__).resolve()
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()
import config as c
marketcap = format(c.market_cap,'.0e')

K = 365 #number of days between each xticks

"""
#Bitcoin prevalence on Cap-weighted

CW_weights_20 = pd.read_csv(f"{path_data_processed}/CW_weights_20_1e{marketcap[-1]}.csv", index_col=0)
CW_weights_100 = pd.read_csv(f"{path_data_processed}/CW_weights_100_1e{marketcap[-1]}.csv", index_col=0)

y20 = CW_weights_20.bitcoin
y100 = CW_weights_100.bitcoin
X = CW_weights_20.index

plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(y20, "b-", label = "Bitcoin weight with 20 cryptocurrencies portfolio")
plt.plot(y100, "r-", label = "Bitcoin weight with 100 cryptocurrencies portfolio")

Xs = X[::K]
xlabels = pd.to_datetime(CW_weights_20.index).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Bitcoin weight in Cap-Weighted portfolio")
plt.ylim(0, 1)
plt.xticks(Xs, xlabels)
plt.legend(loc='lower right')
plt.ylabel('Weight in the Cap-Weighted portfolio')
plt.savefig('graphs/bitcoin_weight.png', format="png")
#plt.show()
plt.clf()
"""
#graphs of low beta perf for different benchmarks

LB=pd.read_csv(f"{path_data_strat}/Low_Beta_price_100_1e{marketcap[-1]}.csv", index_col=0)
HB=pd.read_csv(f"{path_data_strat}/High_Beta_price_100_1e{marketcap[-1]}.csv", index_col=0)
LB_EW=pd.read_csv(f"{path_data_strat}/Low_Beta_EW_price_100_1e{marketcap[-1]}.csv", index_col=0)
HB_EW=pd.read_csv(f"{path_data_strat}/High_Beta_EW_price_100_1e{marketcap[-1]}.csv", index_col=0)
LB_BTC=pd.read_csv(f"{path_data_strat}/Low_Beta_BTC_price_100_1e{marketcap[-1]}.csv", index_col=0)
HB_BTC=pd.read_csv(f"{path_data_strat}/High_Beta_BTC_price_100_1e{marketcap[-1]}.csv", index_col=0)

yLB = np.log(LB)
yLB_EW = np.log(LB_EW)
yLB_BTC = np.log(LB_BTC)
yHB = np.log(HB)
yHB_EW = np.log(HB_EW)
yHB_BTC = np.log(HB_BTC)
X = LB.index

plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(yLB, "b-", alpha=0.8, label = "Low Beta Cap Weighted Benchmark")
plt.plot(yLB_EW, "b--", alpha=0.8, label = "Low Beta Equal Weighted Benchmark")
plt.plot(yLB_BTC, "b:", alpha=0.8, label = "Low Beta Bitcoin Benchmark")
plt.plot(yHB, "r-", alpha=0.8, label = "High Beta Cap Weighted Benchmark")
plt.plot(yHB_EW, "r--", alpha=0.8, label = "High Beta Equal Weighted Benchmark")
plt.plot(yHB_BTC, "r:", alpha=0.8, label = "High Beta Bitcoin Benchmark")

Xs = X[::K]
xlabels = pd.to_datetime(X).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Low Beta comparison between benchmarks")
plt.xticks(Xs, xlabels)
plt.legend(loc='upper left')
plt.ylabel('Log Portfolio Price Performance')
plt.savefig('graphs/low_beta_comp.png', format="png")
plt.show()
plt.clf()


#leverage split table low vol high vol

#Table of Sharpe taking into account turnover at 0.3% per trans

#Graph vola CW and ?
