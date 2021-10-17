import pandas as pd
from datetime import datetime
import os
from tqdm import tqdm

## create file to know first date of crypto ##
crypto = []
first_dates = []
files = os.listdir('./data/')

is_create_file = input('Do you want to create a new file date ? [y/no]')

def create_file():
    for f in tqdm(files[:]):
        try:
            
            #print(f.split(".")[0])
            df = pd.read_pickle(f"data/{f}")
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
    df.to_csv('./first_date_crypto.csv', index=False)

if is_create_file == 'y':
    create_file()

df = pd.read_csv('./first_date_crypto.csv')

bitcoin = df[(df['crypto_name'] == 'bitcoin')]
bitcoin_date = bitcoin['first_date']

#modif here to first newvalue
# create loop inside a with file to find the best matching with first date after bitcoin
other_crypto = df[(df['first_date'] == bitcoin_date.values[0])]
other_crypto.to_csv('./crypto_begin_with_bitcoin.csv')
print(bitcoin)
print(bitcoin_date.values[0])
print(other_crypto.head(5))
