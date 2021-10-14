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

#Environment vars
MARKET_CAP_LIMIT = 1000000000000

#################
#Functions
################

def getMarketcap(crypto, start_date, stop_date):
    mktcap = san.get(
        f"marketcap_usd/{crypto}",
        from_date=start_date,
        to_date=stop_date,
        interval="1d"
        )
    if len(mktcap) > 0:
        return mktcap
    else:
        return 0

def getDf(crypto, start, end):
    df = san.get(
        f"ohlc/{crypto}",
        from_date=start,
        to_date=end,
        interval="1d"
    )
    return df


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

#get dates
def init_date():
    today = date.today()
    stop_date = today.strftime("%Y-%m-%d")
    start_date_raw = today - timedelta(days=1000)
    start_date = start_date_raw.strftime("%Y-%m-%d")
    return (start_date,stop_date)

#get pandas df and merge dat
list_crypto = []
length = 0
total_length = len(cryptoName)
for crypto in cryptoName:
    print(f"{length} out of {total_length}")
    length += 1
    lenDf = 1000
    start_date = init_date()[0]
    stop_date = init_date()[1]


    while(1000 == lenDf):
        df = getDf(f'{crypto}', start_date, stop_date)
        lenDf = len(df)

    list_crypto.append(crypto)
    df.to_pickle(f"data/{crypto}_ohlc.pkl")
    print(f"Successfully stored {crypto}")


with open("data/crypto_list.dat", "wb") as f: #save list of cryptos selected as an object
    pickle.dump(list_crypto, f)
