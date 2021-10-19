import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

number_of_crypto = 20
df_name_index = pd.read_csv(f"./data/processed/crypto_index_{number_of_crypto}.csv", index_col=0)
df = pd.read_csv("./data/processed/market_cap_crypto.csv", index_col=0)
df_close_price = pd.read_csv('./data/processed/close_price_crypto.csv', index_col=0)

data = {}

last_date = df_name_index['first_date'].values[-1]
# print(last_date)
# print(df_name_index.head(5))

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
portfolio_cap_weigthed_index = pd.DataFrame({'cap_weighted_index': cap_weighted_index})
portfolio_cap_weigthed_index.to_csv(f'./data/processed/{number_of_crypto}_portfolio_cap_weighted.csv')
#plt.plot(df_cap_weighted.index, cap_weighted_index)
#plt.show()


###############################
## ponderated index weigthed ##
###############################

## Weigths
##########

df_ponderated = pd.DataFrame(columns=df_final_index.columns[:-1], index= df_final_index.index)
ponderated_values = []
for i in range(len(df_ponderated)):
    ponderated_values.append(1/number_of_crypto)

for column in df_ponderated:
    df_ponderated[column] = ponderated_values

## Ponderated Index
#####################

ponderated_index = np.sum(np.multiply(df_close_price_index.values,df_ponderated.values), 1)
portfolio_ponderated_index = pd.DataFrame({'ponderated_index': ponderated_index})
portfolio_ponderated_index.to_csv(f'./data/processed/{number_of_crypto}_portfolio_ponderated.csv')
# plt.plot(df_ponderated.index, ponderated_index)
# plt.show()