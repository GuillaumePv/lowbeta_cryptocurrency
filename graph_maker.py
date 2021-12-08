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


#Bitcoin prevalence on Cap-weighted
"""
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
"""

#Table of Sharpe taking into account turnover at 0.3% per trans

metrics_20 = pd.read_csv(f"{path_data_processed}/df_metrics_20_1e{marketcap[-1]}.csv", index_col=0)
metrics_100 = pd.read_csv(f"{path_data_processed}/df_metrics_100_1e{marketcap[-1]}.csv", index_col=0)

rf_monthly = metrics_20.iloc[0, 0] - metrics_20.iloc[0, 2] * metrics_20.iloc[0, 1] #reverse engineer rf from metrics sharpe

metrics_20['sharpe_adj'] = (metrics_20.monthly_returns - metrics_20.monthly_turnover * 0.003 - rf_monthly) / metrics_20.volatility
metrics_100['sharpe_adj'] = (metrics_100.monthly_returns - metrics_100.monthly_turnover * 0.003 - rf_monthly) / metrics_100.volatility

df_sharpe = pd.DataFrame(columns = metrics_20.index)
df_sharpe.loc['Sharpe 20 adjusted'] = metrics_20.sharpe_adj.values.round(3)
df_sharpe.loc['Sharpe 100 adjusted'] = metrics_100.sharpe_adj.values.round(3)
print(df_sharpe)
df_sharpe.to_latex("latex/sharpe_adj")

metrics_20 = pd.read_csv(f"{path_data_processed}/df_metrics_20_1e{marketcap[-1]}_reb7.csv", index_col=0)
metrics_100 = pd.read_csv(f"{path_data_processed}/df_metrics_100_1e{marketcap[-1]}_reb7.csv", index_col=0)

rf_monthly = metrics_20.iloc[0, 0] - metrics_20.iloc[0, 2] * metrics_20.iloc[0, 1] #reverse engineer rf from metrics sharpe

metrics_20['sharpe_adj'] = (metrics_20.monthly_returns - metrics_20.monthly_turnover * 0.003 - rf_monthly) / metrics_20.volatility
metrics_100['sharpe_adj'] = (metrics_100.monthly_returns - metrics_100.monthly_turnover * 0.003 - rf_monthly) / metrics_100.volatility

df_sharpe = pd.DataFrame(columns = metrics_20.index)
df_sharpe.loc['Sharpe 20 rebalanced 7 adjusted'] = metrics_20.sharpe_adj.values.round(3)
df_sharpe.loc['Sharpe 100 rebalanced 7 adjusted'] = metrics_100.sharpe_adj.values.round(3)
print(df_sharpe)
df_sharpe.to_latex("latex/sharpe_adj_reb7")


metrics_20 = pd.read_csv(f"{path_data_processed}/df_metrics_20_1e{marketcap[-1]}_reb30.csv", index_col=0)
metrics_100 = pd.read_csv(f"{path_data_processed}/df_metrics_100_1e{marketcap[-1]}_reb30.csv", index_col=0)

rf_monthly = metrics_20.iloc[0, 0] - metrics_20.iloc[0, 2] * metrics_20.iloc[0, 1] #reverse engineer rf from metrics sharpe

metrics_20['sharpe_adj'] = (metrics_20.monthly_returns - metrics_20.monthly_turnover * 0.003 - rf_monthly) / metrics_20.volatility
metrics_100['sharpe_adj'] = (metrics_100.monthly_returns - metrics_100.monthly_turnover * 0.003 - rf_monthly) / metrics_100.volatility

df_sharpe = pd.DataFrame(columns = metrics_20.index)
df_sharpe.loc['Sharpe 20 rebalanced 30 adjusted'] = metrics_20.sharpe_adj.values.round(3)
df_sharpe.loc['Sharpe 100 rebalanced 30 adjusted'] = metrics_100.sharpe_adj.values.round(3)
print(df_sharpe)
df_sharpe.to_latex("latex/sharpe_adj_reb30")

#Graph vola CW and ?
