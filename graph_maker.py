from sys import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import plotly.express as px

path_original = Path(__file__).resolve()
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

import config as c
marketcap = format(c.market_cap,'.0e')

K = 365 #number of days between each xticks

#############
### Graphs ##
#############

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


plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
fig, ax = plt.subplots(figsize=(6.4 * 2, 4.8 * 1.2))
ax.stackplot(y20.index, y20, alpha=0.8)
ax.legend(loc='upper left')
plt.xticks(Xs, xlabels)
ax.set_title('Bitcoin weight in Cap-Weighted portfolio (20 Cryptos)')
ax.set_xlabel('Date')
ax.set_ylabel('Weight in the Cap-Weighted portfolio')
plt.savefig('graphs/bitcoin_weight_stack_20.png', format="png")


Xs = X[::K]
xlabels = pd.to_datetime(y100.index).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
fig, ax = plt.subplots(figsize=(6.4 * 2, 4.8 * 1.2))
ax.stackplot(pd.to_datetime(y100.index), y100, alpha=0.8, color="red")
ax.legend(loc='upper left')
# plt.xticks(Xs, xlabels)
ax.set_title('Bitcoin weight in Cap-Weighted portfolio (100 Cryptos)')
ax.set_xlabel('Date')
ax.set_ylabel('Weight in the Cap-Weighted portfolio')
plt.savefig('graphs/bitcoin_weight_stack_100.png', format="png")
print(y100.index)

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
# plt.show()
plt.clf()


## Low Vol ##

LV = pd.read_csv(f"{path_data_strat}/Low_Vol_price_100_1e{marketcap[-1]}.csv", index_col=0)
HV = pd.read_csv(f"{path_data_strat}/High_Vol_price_100_1e{marketcap[-1]}.csv", index_col=0)

yLV = np.log(LV)
yHV = np.log(HV)


X = HV.index
plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(yLV, "b-", alpha=0.8, label = "Low Volatility")
plt.plot(yHV, "r--", alpha=0.8, label = "High Volatility")

Xs = X[::K]
xlabels = pd.to_datetime(X).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Performance of Low volatility strategy (100 Cryptocurrencies)")
plt.xticks(Xs, xlabels)
plt.legend(loc='upper left')
plt.ylabel('Log Portfolio Price Performance')
plt.savefig('graphs/low_vol_100.png', format="png")


LV = pd.read_csv(f"{path_data_strat}/Low_Vol_price_20_1e{marketcap[-1]}.csv", index_col=0)
HV = pd.read_csv(f"{path_data_strat}/High_Vol_price_20_1e{marketcap[-1]}.csv", index_col=0)

yLV = np.log(LV)
yHV = np.log(HV)


X = HV.index
plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(yLV, "b-", alpha=0.8, label = "Low Volatility")
plt.plot(yHV, "r--", alpha=0.8, label = "High Volatility")

Xs = X[::K]
xlabels = pd.to_datetime(X).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Performance of Low volatility strategy (100 Cryptocurrencies)")
plt.xticks(Xs, xlabels)
plt.legend(loc='upper left')
plt.ylabel('Log Portfolio Price Performance')
plt.savefig('graphs/low_vol_20.png', format="png")

## Minimum Variance ##

MV_20 = pd.read_csv(f"{path_data_strat}/MV_price_20_1e{marketcap[-1]}.csv", index_col=0)
MV_100 = pd.read_csv(f"{path_data_strat}/MV_price_100_1e{marketcap[-1]}.csv", index_col=0)

CW_20 = pd.read_csv(f"{path_data_strat}/CW_price_20_1e{marketcap[-1]}.csv", index_col=0)
dif_20 = CW_20.shape[0] - MV_20.shape[0]
CW_20 = CW_20.iloc[dif_20:,:]

CW_100 = pd.read_csv(f"{path_data_processed}/CW_perf_100_1e{marketcap[-1]}.csv", index_col=0)
dif_100 = CW_100.shape[0] - MV_100.shape[0]
CW_100 = CW_100.iloc[dif_100:,:]
CW_100 = CW_100.add(1).cumprod()*100

yMV_20 = np.log(MV_20)
yCW_20 = np.log(CW_20)
X = CW_20.index

plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(yMV_20, "b-", alpha=0.8, label = "Minimum Variance")
plt.plot(yCW_20, "r--", alpha=0.8, label = "Cap-weigthed benchmark")

Xs = X[::K]
xlabels = pd.to_datetime(X).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Performance of Minimum Variance (20 Cryptocurrencies)")
plt.xticks(Xs, xlabels)
plt.legend(loc='upper left')
plt.ylabel('Log Portfolio Price Performance')
plt.savefig('graphs/min_var_vs_cap_weigthed_20.png', format="png")


yMV_100 = np.log(MV_100)
yCW_100 = np.log(CW_100)
X = CW_100.index

plt.figure(figsize=(6.4 * 2, 4.8 * 1.2))
plt.plot(yMV_100, "b-", alpha=0.8, label = "Minimum Variance")
plt.plot(yCW_100, "r--", alpha=0.8, label = "Cap-weigthed benchmark")

Xs = X[::K]
xlabels = pd.to_datetime(X).strftime("%Y-%m")
xlabels = xlabels[::K]
plt.title("Performance of Minimum Variance (100 Cryptocurrencies)")
plt.xticks(Xs, xlabels)
plt.legend(loc='upper left')
plt.ylabel('Log Portfolio Price Performance')
plt.savefig('graphs/min_var_vs_cap_weigthed_100.png', format="png")
###########
## Table ##
###########

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
df_sharpe.to_latex("latex/sharpe_adj.tex", caption="Sharpe Ratios of strategies adjusted for turnover", label="sharpe", float_format="%.2f" )

metrics_20 = pd.read_csv(f"{path_data_processed}/df_metrics_20_1e{marketcap[-1]}_reb7.csv", index_col=0)
metrics_100 = pd.read_csv(f"{path_data_processed}/df_metrics_100_1e{marketcap[-1]}_reb7.csv", index_col=0)

rf_monthly = metrics_20.iloc[0, 0] - metrics_20.iloc[0, 2] * metrics_20.iloc[0, 1] #reverse engineer rf from metrics sharpe

metrics_20['sharpe_adj'] = (metrics_20.monthly_returns - metrics_20.monthly_turnover * 0.003 - rf_monthly) / metrics_20.volatility
metrics_100['sharpe_adj'] = (metrics_100.monthly_returns - metrics_100.monthly_turnover * 0.003 - rf_monthly) / metrics_100.volatility

df_sharpe = pd.DataFrame(columns = metrics_20.index)
df_sharpe.loc['Sharpe 20 rebalanced 7 adjusted'] = metrics_20.sharpe_adj.values.round(3)
df_sharpe.loc['Sharpe 100 rebalanced 7 adjusted'] = metrics_100.sharpe_adj.values.round(3)
# print(df_sharpe)
df_sharpe.to_latex("latex/sharpe_adj_reb7.tex", caption="Sharpe Ratio of strategies adjusted for turnover (Rebalanced 7 days)", label="sharpe7", float_format="%.2f" )


metrics_20 = pd.read_csv(f"{path_data_processed}/df_metrics_20_1e{marketcap[-1]}_reb30.csv", index_col=0)
metrics_100 = pd.read_csv(f"{path_data_processed}/df_metrics_100_1e{marketcap[-1]}_reb30.csv", index_col=0)

rf_monthly = metrics_20.iloc[0, 0] - metrics_20.iloc[0, 2] * metrics_20.iloc[0, 1] #reverse engineer rf from metrics sharpe

metrics_20['sharpe_adj'] = (metrics_20.monthly_returns - metrics_20.monthly_turnover * 0.003 - rf_monthly) / metrics_20.volatility
metrics_100['sharpe_adj'] = (metrics_100.monthly_returns - metrics_100.monthly_turnover * 0.003 - rf_monthly) / metrics_100.volatility

df_sharpe = pd.DataFrame(columns = metrics_20.index)
df_sharpe.loc['Sharpe 20 rebalanced 30 adjusted'] = metrics_20.sharpe_adj.values.round(3)
df_sharpe.loc['Sharpe 100 rebalanced 30 adjusted'] = metrics_100.sharpe_adj.values.round(3)
# print(df_sharpe)
df_sharpe.to_latex("latex/sharpe_adj_reb30.tex", caption="Sharpe Ratio of strategies adjusted for turnover (Rebalanced 30 days)", label="sharpe30", float_format="%.2f" )

#Graph vola CW and ?
