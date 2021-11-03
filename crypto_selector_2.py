# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from datetime import datetime
from datetime import timedelta
import os
from tqdm import tqdm

## create file to know first date of crypto ##
crypto = []
first_dates = []
files = os.listdir('./data/raw/')

is_create_file = input('Do you want to create a new file date ? [y/no]')


for f in tqdm(files[:]):
    try:

            #print(f.split(".")[0])
        df = pd.read_pickle(f"./data/raw/{f}")
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
df.to_csv('./data/processed/first_date_crypto_list_sorted.csv')

# %% [markdown]
# # code to find market cap 1 mio$ date

# %%
test_marketcap = 1e9 #paper ruben

list_market_1mio = []
list_crypto = []
for f in tqdm(files[:]):
    try:

            #print(f.split(".")[0])
        df = pd.read_pickle(f"./data/raw/{f}")
            #print(df.head(5))
        df['Condition'] = df['marketcap'] >= test_marketcap
        index = df[df.Condition!=False].first_valid_index()
        if index is not None:
            date = datetime.date(df.index[0])
            list_market_1mio.append(date)
            list_crypto.append(f.split(".")[0])
        
    except Exception:
        continue

data = {
        "crypto_name":list_crypto,
        "first_date_marketcap_1mio":list_market_1mio
}

df_market_cap = pd.DataFrame(data)
df_market_cap = df_market_cap.sort_values('first_date_marketcap_1mio')
df_market_cap.to_csv('./data/processed/crypto_date_marketcap_1mio_sorted.csv')


