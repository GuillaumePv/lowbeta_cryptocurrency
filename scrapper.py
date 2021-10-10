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
NUMBER_YEARS_CUTOFF = 4
MARKET_CAP_LIMIT = 100000000

#################
#Functions
################

def getMarketcap(crypto="bitcoin"):
    mktcap = san.get(
        f"marketcap_usd/{crypto}",
        from_date=start_date,
        to_date=stop_date
        )
    if len(mktcap) > 0:
        return mktcap.value[-1]
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
today = date.today()
stop_date = today.strftime("%Y-%m-%d")
start_date_raw = today - relativedelta(years=NUMBER_YEARS_CUTOFF)
start_date = start_date_raw.strftime("%Y-%m-%d")
delta = today - start_date_raw
delta_days = delta.days + 1

#get pandas df and filter/save
list_crypto = []
length = 0
total_length = len(cryptoName)
for crypto in cryptoName:
    print(f"{length} out of {total_length}")
    length += 1

    mktcap = getMarketcap(f'{crypto}')
    if mktcap <= MARKET_CAP_LIMIT:
        continue

    df = getDf(f'{crypto}', start_date, stop_date)
    if len(df) == delta_days:
        list_crypto.append(crypto)
        df.to_pickle(f"data/{crypto}_ohlc.pkl")
        print(f"Successfully stored {crypto}")


with open("data/crypto_list.dat", "wb") as f: #save list of cryptos selected as an object
    pickle.dump(list_crypto, f)
