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

def create_file():
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
    df.to_csv('./data/processed/first_date_crypto.csv', index=False)

if is_create_file == 'y':
    create_file()

df = pd.read_pickle('./data/raw/bitcoin.pkl')

df_date = pd.read_csv('./data/processed/first_date_crypto.csv')

bitcoin = df.index[0]

#need to string to compare with csv
bitcoin_date = datetime.date(df.index[0])
bitcoin_end = datetime.date(df.index[-1])

#modif here to first newvalue
# create loop inside a with file to find the best matching with first date after bitcoin

## change to obtain first 20 and 100
print(bitcoin_date,bitcoin_end)
other_crypto = df_date[(df_date['first_date'] == str(bitcoin_date))]
print("Crypto number: ",len(other_crypto))


print(len(other_crypto))
print(bitcoin_date)

i = 0
number_of_crypto = 20
while len(other_crypto) < number_of_crypto:

    df_test = df_date[(df_date['first_date'] == str(bitcoin_date))]
    #print(len(df_test))
    for value in df_test['crypto_name']:
        df_crypto = pd.read_pickle(f'./data/raw/{value}.pkl')
        date = str(datetime.date(df_crypto.index[-1]))

        if date == str(bitcoin_end):
            if value == 'bitcoin' or value == 'litecoin' or value == 'namecoin':
                continue
            else:
                data = {
                    'crypto_name':value,
                    'first_date': datetime.date(df_crypto.index[0])
                }
                other_crypto = other_crypto.append(data, ignore_index=True)
#         print(value)
    bitcoin_date = bitcoin_date + timedelta(days=1)
    #print(len(other_crypto))

other_crypto.to_csv(f'./data/processed/crypto_index_{number_of_crypto}.csv')


## select only data from the last
# for value in other_crypto['crypto_name']:
#     df_crypto = pd.read_pickle(f'./data/raw/{value}.pkl')
#     date = str(datetime.date(df_crypto.index[-1]))

#     if date == str(bitcoin_end):
#         print(value)

# print(other_crypto)
# #other_crypto.to_csv('./data/processed/crypto_begin_with_bitcoin.csv')
# print(bitcoin)
# print(bitcoin_date)
# print(other_crypto.head(5))
