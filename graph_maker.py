import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
path_original = Path(__file__).resolve()
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()
import config as c
marketcap = format(c.market_cap,'.0e')

K = 180 #number of days between each xticks


#Bitcoin prevalence on Cap-weighted

CW_weights_20 = pd.read_csv(f"{path_data_processed}/CW_weights_20_1e{marketcap[-1]}.csv", index_col=0)
CW_weights_100 = pd.read_csv(f"{path_data_processed}/CW_weights_100_1e{marketcap[-1]}.csv", index_col=0)

y20 = CW_weights_20.bitcoin
y100 = CW_weights_100.bitcoin
X = CW_weights_20.index

plt.figure(figsize=(6.4 * 2, 4.8 * 1))
plt.plot(y20, "b-", label = "Bitcoin weight with 20 cryptocurrencies portfolio")
plt.plot(y100, "r-", label = "Bitcoin weight with 100 cryptocurrencies portfolio")

Xs = CW_weights_20.index[::K]
xlabels = pd.to_datetime(CW_weights_20.index).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Bitcoin weight in Cap-Weighted portfolio")
plt.xticks(rotation=50)
plt.ylim(0, 1)
plt.xticks(Xs, xlabels)
plt.legend(loc='lower right')
plt.ylabel('Weight in the Cap-Weighted portfolio')
plt.show()
plt.savefig('graphs/bitcoin_weight.jpeg')

#Tables of metrics for every rebalancement


#Graphs of perfs 20 and 100

#leverage split table low vol high vol

#Table of Sharpe taking into account turnover at 0.3% per trans

#Graph vola CW and ?
