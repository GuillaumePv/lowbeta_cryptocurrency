import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

number_of_crypto = 20
df_name_index = pd.read_csv(f"./data/processed/first_{number_of_crypto}_crypto_list.csv", index_col=0)
df = pd.read_csv("./data/processed/market_cap_crypto.csv", index_col=0)
df_close_price = pd.read_csv('./data/processed/close_price_crypto.csv', index_col=0)

data = {}

last_date = df_name_index['first_date'].values[-1]

columns = df_name_index['crypto_name']
print(columns)
df_index = df[columns]
df_index['total_market_cap'] = df_index.sum(axis=1)
df_index.index = pd.to_datetime(df_index.index)

list_index = []
for i in range(len(df_index.index)):
    v = pd.to_datetime(datetime.date(df_index.index[i]))
    list_index.append(v)

list_index = np.array(list_index)

last_date = pd.to_datetime(last_date)

index = np.where(list_index == last_date)[0][0]

df_final_index = df_index.iloc[index:,:]
df_close_price = df_close_price[columns]
df_close_price_index = df_close_price.iloc[index:,:]


########################
## cap weighted index ##
########################

df_cap_weighted = df_final_index

## Weigths
##########
for column in df_cap_weighted.columns[:-1]:
    try:
        df_cap_weighted[column] = df_final_index[column]/df_final_index['total_market_cap']
    except Exception as e:
        values = []
        for i in range(len(df_final_index[column])):
            v = df_final_index[column].values[i] / df_final_index['total_market_cap'].values[i]
            values.append(v)
        df_cap_weighted[column] = values

df_cap_weighted = df_cap_weighted.iloc[:,:-1]
        #print(str(e))

## Cap-weigthed Index
#####################

cap_weighted_index = np.sum(np.multiply(df_close_price_index.values,df_cap_weighted.values), 1)
portfolio_cap_weigthed_index = pd.DataFrame({'cap_weighted_index': cap_weighted_index},index=df_cap_weighted.index)
portfolio_cap_weigthed_index['date'] = pd.to_datetime(portfolio_cap_weigthed_index.index)
portfolio_cap_weigthed_index['date'] = portfolio_cap_weigthed_index['date'].dt.date
portfolio_cap_weigthed_index.index = portfolio_cap_weigthed_index['date']
del portfolio_cap_weigthed_index['date']

portfolio_cap_weigthed_index.to_csv(f'./data/processed/CW_{number_of_crypto}_price.csv')
perf_cap_weigthed = np.log(portfolio_cap_weigthed_index/portfolio_cap_weigthed_index.shift(1)).dropna()
perf_cap_weigthed.to_csv(f'./data/processed/perf_CW_{number_of_crypto}_price.csv',index=True)
#plt.plot(df_cap_weighted.index, cap_weighted_index)
#plt.show()


###############################
## ponderated index weigthed ##
###############################

## Weigths
##########

df_equal_weigthed = pd.DataFrame(columns=df_final_index.columns[:-1], index= df_final_index.index)
equal_weigthed_values = []
for i in range(len(df_equal_weigthed)):
    equal_weigthed_values.append(1/number_of_crypto)

for column in df_equal_weigthed:
    df_equal_weigthed[column] = equal_weigthed_values

## Ponderated Index
#####################

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

