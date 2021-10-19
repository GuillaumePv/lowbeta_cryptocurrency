import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime
import numpy as np

number_of_crypto = 20
df_name_index = pd.read_csv(f"./data/processed/crypto_index_{number_of_crypto}.csv", index_col=0)
df = pd.read_csv("./data/processed/market_cap_crypto.csv", index_col=0)
data = {}

last_date = df_name_index['first_date'].values[-1]
# print(last_date)
# print(df_name_index.head(5))

columns = df_name_index['crypto_name']

df_index = df[columns]
df_index['total_market_cap'] = df_index.sum(axis=1)
df_index.index = pd.to_datetime(df_index.index)

list_index = []
for i in range(len(df_index.index)):
    v = pd.to_datetime(datetime.date(df_index.index[i]))
    list_index.append(v)

list_index = np.array(list_index)
# print(list_index)
last_date = pd.to_datetime(last_date)
# print(last_date)

index = np.where(list_index == last_date)[0][0]
# print(index)
df_final_index = df_index.iloc[index:,:]
#print(df_final_index.head(5))

df_cap_weighted = df_final_index

## cap weigted
## bug for some crypto 
for column in df_cap_weighted.columns[:]:
    # print(df_cap_weighted[column])
    #print(df_final_index[column])
    print(column)
    try:
        print(df_final_index[column]/df_final_index['total_market_cap'])
    except Exception as e:
        print(str(e))



###############################
## ponderated index weigthed ##
###############################

df_ponderated = pd.DataFrame(columns=df_final_index.columns[:-1], index= df_final_index.index)
ponderated_values = []
for i in range(len(df_ponderated)):
    ponderated_values.append(1/number_of_crypto)

for column in df_ponderated:
    df_ponderated[column] = ponderated_values

