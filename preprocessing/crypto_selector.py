print(40*"=")
print("crypto_selector")
print(40*"=")

import pandas as pd
from datetime import datetime
from datetime import timedelta

from tqdm import tqdm

import os
import sys
import inspect
sys.path.insert(1, os.path.realpath(os.path.pardir))

import config as c

## create file to know first date of crypto ##
crypto = []
first_dates = []
files = os.listdir('../data/raw/')

for f in tqdm(files[:]):
    try:
        #print(f.split(".")[0])
        df = pd.read_pickle(f"../data/raw/{f}")
        #print(df.head(5))
        date = datetime.date(df.index[0])
        first_dates.append(date)
        crypto.append(f.split(".")[0])
    except Exception:
        continue

data = {
        "crypto_name":crypto,
        "first_date":first_dates
}

df = pd.DataFrame(data)
df = df.sort_values('first_date')
df.reset_index(inplace=True, drop=True)
df.to_csv('../data/processed/first_date_crypto_list_sorted.csv')


#get first date of appearence of the set market_cap
####################################################

test_marketcap = c.market_cap #paper ruben

list_market = []
list_crypto = []
for f in tqdm(files[:]):
    try:
        #print(f.split(".")[0])
        df = pd.read_pickle(f"../data/raw/{f}")
        #print(df.head(5))
        df['Condition'] = df['marketcap'] >= test_marketcap
        index = df[df.Condition!=False].first_valid_index()
        if index is not None:
            date = datetime.date(df.index[0])
            list_market.append(date)
            list_crypto.append(f.split(".")[0])
    except Exception:
        continue

data = {
        "crypto_name":list_crypto,
        "first_date_marketcap":list_market
}

df_market_cap = pd.DataFrame(data)
df_market_cap = df_market_cap.sort_values('first_date_marketcap')
marketcap = format(c.market_cap,'.0e')
df_market_cap.to_csv(f'../data/processed/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv')
