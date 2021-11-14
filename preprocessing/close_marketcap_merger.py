import pandas as pd
from datetime import datetime
from  tqdm import tqdm
import os

#message for makefile
print(40*"=")
print("STARTING PREPROCESSING")
print(40*"=")

df = pd.read_pickle(f"../data/raw/bitcoin.pkl")
print(df.head(5))

files = os.listdir('../data/raw/')

df_base = pd.read_pickle(f"../data/raw/{files[0]}")
name_first_file = files[0].split(".")[0]
df_base[name_first_file] = df_base['marketcap']
#print(df_base.head(5))
df_base_price = df_base['closePriceUsd']
df_base = df_base[name_first_file]

#print(df_base.head(3))
list_crypto = [name_first_file]
for f in tqdm(files[1:]):
    try:

        crypto = f.split(".")[0]
        df = pd.read_pickle(f"../data/raw/{f}")
        date_index = df.index
        df[crypto] = df['marketcap']
        #market_cap = df['marketcap']
        close_price = df['closePriceUsd']
        df_base = pd.concat([df_base,df[crypto]], ignore_index=True, axis=1)
        df_base_price = pd.concat([df_base_price,df['closePriceUsd']], ignore_index=True, axis=1)
        list_crypto.append(crypto)
    except Exception as e:
        print(str(e))
        continue

#fill na => see impact on
df_base.columns = list_crypto
df_base = df_base.fillna(0)
# df_base['total_market_cap'] = df_base.sum(axis=1)
df_base_price.columns = list_crypto
df_base_price = df_base_price.fillna(0)
# print(df_base.head(4))

df_base.to_csv('../data/processed/market_cap_crypto.csv', index=True,)
df_base_price.to_csv('../data/processed/close_price_crypto.csv', index=True)
