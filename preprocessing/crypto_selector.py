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
