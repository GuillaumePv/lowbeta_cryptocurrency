#Basic Utilities
import pandas
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#file management
import pickle
import os
import glob

#Data fetchers
import san

#################
#Functions
################
def getDf(crypto, start, end):
    df = san.get(
        f"ohlc/{crypto}",
        from_date=start,
        to_date=end,
        interval="1d"
    )
    return df

#get dates
def init_date(days_delta=0):
    today = date.today() - timedelta(days=days_delta)
    stop_date = today.strftime("%Y-%m-%d")
    start_date_raw = today - timedelta(days=1000) - timedelta(days=days_delta) #1000 days is the limit for ohlc requests
    start_date = start_date_raw.strftime("%Y-%m-%d")
    return (start_date,stop_date)


#################
#Script
#################
print(40*"=")
print("Starting script...")

#remove old files
print('Do you want to remove old files? (Type y if yes)')
y = input()
if y == "y":
    files = glob.glob('data/*')
    for f in files:
        os.remove(f)

#finds all crypto names
cryptoName = san.get("projects/all").slug


#get pandas df and merge dat
list_crypto = []
length = 0
total_length = len(cryptoName)
start_date, stop_date = init_date()
lenDf = 1000

for crypto in cryptoName:
    print(f"{length} out of {total_length}")
    length += 1
    start_date_mod = start_date
    stop_date_mod = stop_date
    loop_number = 0
    dfAll = pd.DataFrame()

    while(1000 == lenDf):
        start_date_mod, stop_date_mod = init_date(days_delta = loop_number*1000)
        df = getDf(f'{crypto}', start_date_mod, stop_date_mod)
        lenDf = len(df)
        if lenDf > 0:
            dfAll = dfAll.append(df)
        loop_number += 1


    list_crypto.append(crypto)
    dfAll.to_pickle(f"data/{crypto}_ohlc.pkl")
    print(f"Successfully stored {crypto}")


with open("data/crypto_list.dat", "wb") as f: #save list of cryptos selected as an object
    pickle.dump(list_crypto, f)
