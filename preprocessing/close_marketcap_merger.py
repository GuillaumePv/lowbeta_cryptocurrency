###############################################
# Creates aggregate close and market
# capitalization files for cryptocurrencies
###############################################

#utilities
import pandas as pd
import os
from datetime import datetime
from  tqdm import tqdm
from pathlib import Path

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data = (path_original / "../data/raw/").resolve()
path_data_processed = (path_original / "../data/processed/").resolve()

#message for makefile
print(40*"=")
print("STARTING PREPROCESSING")
print(40*"=")

print(40*"=")
print("close_marketcap_merger")
print(40*"=")

df = pd.read_pickle(f"{path_data}/bitcoin.pkl")

files = os.listdir(f'{path_data}')

#create file shell with first raw file
df_base = pd.read_pickle(f"{path_data}/{files[0]}")
name_first_file = files[0].split(".")[0]
df_base[name_first_file] = df_base['marketcap']

df_base_price = df_base['closePriceUsd']
df_base_volume = df_base['volume']
df_base = df_base[name_first_file]

#add all cryptos
list_crypto = [name_first_file]
for f in tqdm(files[1:]):
    try:
        crypto = f.split(".")[0]
        df = pd.read_pickle(f"{path_data}/{f}")
        date_index = df.index
        df[crypto] = df['marketcap']
        close_price = df['closePriceUsd']
        df_base = pd.concat([df_base,df[crypto]], ignore_index=True, axis=1)
        df_base_price = pd.concat([df_base_price,df['closePriceUsd']], ignore_index=True, axis=1)
        df_base_volume = pd.concat([df_base_volume,df['volume']], ignore_index=True, axis=1)
        list_crypto.append(crypto)
    except Exception as e:
        print(str(e))
        continue

#data cleaning
df_base.columns = list_crypto
df_base = df_base.fillna(0)
df_base_price.columns = list_crypto
df_base_price = df_base_price.fillna(0)


#store the data
df_base_volume.columns = list_crypto
df_base_volume = df_base_volume.fillna(0)

df_base.to_csv(f'{path_data_processed}/market_cap_crypto.csv', index=True,)
df_base_price.to_csv(f'{path_data_processed}/close_price_crypto.csv', index=True)
df_base_volume.to_csv(f'{path_data_processed}/volume_price_crypto.csv', index=True)
