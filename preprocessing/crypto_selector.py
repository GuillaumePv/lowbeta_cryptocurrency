###############################################
# Finds first data of appearence of each
# crypto + first time they get to threshold
###############################################

print(40*"=")
print("crypto_selector")
print(40*"=")

#utilities
import pandas as pd
import os
import sys
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
from pathlib import Path

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data = (path_original / "../data/raw/").resolve()
path_data_processed = (path_original / "../data/processed/").resolve()

# set up paths
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import config as c



#create file to know first date of crypto appearence
####################################################

crypto = []
first_dates = []
files = os.listdir(path_data)

for f in tqdm(files[:]):
    try:
        df = pd.read_pickle(f"{path_data}/{f}")
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
df.to_csv(f'{path_data_processed}/first_date_crypto_list_sorted.csv')


#get first date of appearence of crypto for the set market_cap
##############################################################

test_marketcap = c.market_cap #paper ruben

list_market = []
list_crypto = []
for f in tqdm(files[:]):
    try:
        df = pd.read_pickle(f"{path_data}/{f}")
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
df_market_cap.to_csv(f'{path_data_processed}/crypto_date_marketcap_sorted_1e{marketcap[-1]}.csv')
