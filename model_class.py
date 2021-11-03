#Utilities
import pandas as pd
import numpy as np
import math
from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_data

class Model:
    def __init__(self, number_cryptos=20, rebalance='daily'):
        self.number_cryptos = number_cryptos
        self.rebalance = rebalance
        self.index = pd.read_csv(f'./data/processed/CV_{self.number_cryptos}_price.csv')
        self.EW = pd.DataFrame()
        self.MVP = pd.DataFrame()
        self.LowBeta = pd.DataFrame()
        self.crypto_name = pd.read_csv(f"./data/processed/first_{self.number_cryptos}_crypto_list.csv", index_col=0)
        self.df_marketcap = pd.read_csv("./data/processed/market_cap_crypto.csv", index_col=0)
        self.df_close_price = pd.read_csv('./data/processed/close_price_crypto.csv', index_col=0)

    def create_EW(self):
        equal_weigthed_index = np.sum(np.multiply(df_close_price_index.values,df_equal_weigthed.values), 1)
        portfolio_equal_weigthed_index = pd.DataFrame({'ponderated_index': equal_weigthed_index},index=df_equal_weigthed.index)
        portfolio_equal_weigthed_index['date'] = pd.to_datetime(portfolio_equal_weigthed_index.index)
        portfolio_equal_weigthed_index['date'] = portfolio_equal_weigthed_index['date'].dt.date
        portfolio_equal_weigthed_index.index = portfolio_equal_weigthed_index['date']
        del portfolio_equal_weigthed_index['date']

        portfolio_equal_weigthed_index.to_csv(f'./data/processed/EW_{number_of_crypto}_price.csv')
        perf_equally_weighted = np.log(portfolio_equal_weigthed_index/portfolio_equal_weigthed_index.shift(1)).dropna()
        perf_equally_weighted.to_csv(f'./data/processed/perf_EW_{number_of_crypto}_price.csv',index=True)
        # plt.plot(df_ponderated.index, ponderated_index)

    def create_min_var(self):
        return 0


    def get_metrics(self):
        df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
        #Rolling Volatility
        df['rol_vol_120'] = df.pct_change().rolling(120).std()
        df.dropna(inplace=True)
        df_metrics.iloc[idx_metric, 1] = df['rol_vol_120'].mean() * math.sqrt(365/12)

        #Total return
        first_date = df.index[0] + relativedelta(day=31)
        df_trunc = df.loc[first_date:]
        number_of_months = int((df_trunc.index[-1] - first_date)/np.timedelta64(1,'M'))
        last_day_months = pd.date_range(start=first_date, periods=number_of_months, freq='M')
        df_month = df_trunc.loc[last_day_months, :]
        df_month['returns'] = (df_month.iloc[:, 0] - df_month.iloc[:, 0].shift())/df_month.iloc[:, 0]
        df_metrics.iloc[idx_metric, 0] = df_month['returns'].mean()
        #Excess returns over benchmark
        if idx_metric != 0:
            df_metrics.iloc[idx_metric, 3] = df_metrics.iloc[idx_metric, 0] - df_metrics.iloc[0, 0]
        else:
            df_metrics.iloc[idx_metric, 3] = 0

        #sharpe
        last_date=df.index[-1].strftime("%Y-%m-%d")
        rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
        if rf == 0: #if rf is not available
            last_date=df.index[-20].strftime("%Y-%m-%d") #get the 20 last days and it will be
            rf = get_data("^TNX", start_date=last_date).adjclose.dropna()[0]
        rf_monthly = pow(rf/100 + 1, 1/12) - 1
        df_metrics.iloc[idx_metric, 2] = (df_metrics.iloc[idx_metric, 0] - rf_monthly)/df_metrics.iloc[idx_metric, 1]

        #beta
        bench_returns = CW.cap_weighted_index.pct_change()
        df_cov = pd.DataFrame({'CW':bench_returns.values, 'df_returns': df.iloc[:, 0].pct_change().values})
        df_cov.dropna(inplace=True)
        cov = df_cov.cov().iloc[0,1]
        beta = cov/pow(df.iloc[:, 0].pct_change().std(),2)
        df_metrics.iloc[idx_metric, 4] = beta

        #Max drawdown
        max_drawdown=min(df.iloc[:,0].pct_change().dropna().values)
        df_metrics.iloc[idx_metric, 5] = max_drawdown

        #hit_ratio
        #Tracking error
        #Information ratio
        #One-Way Turnover
        print(df_metrics)
        df_metrics.to_csv(f'data/processed/df_metrics_{NUMBER_OF_CRYPTOS}.csv')
