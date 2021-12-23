###############################################
# Raw data fetcher
###############################################


#Basic Utilities
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#file management
import pickle
import os
import glob

#Data fetchers
import san


#Functions
################

def getDf(crypto, start, end):
    try:
        df = san.get(
            f"ohlcv/{crypto}",
            from_date=start,
            to_date=end,
            interval="1d"
        )
        return df
    except Exception as e:
        print(e)

#dates management
def init_date(days_delta=0):
    today = date.today()
    stop_date_raw = today - timedelta(days=days_delta)
    stop_date = stop_date_raw.strftime("%Y-%m-%d")
    start_date_raw = today - timedelta(days=999) - timedelta(days=days_delta) #1000 days is the limit for ohlc requests
    start_date = start_date_raw.strftime("%Y-%m-%d")
    return (start_date,stop_date)



#Script
#################
print(40*"=")
print("Starting script...")

#remove old files
print('Do you want to remove old files? (Type y if yes)')
y = input()
if y == "y":
    files = glob.glob('data/raw/*')
    for f in files:
        os.remove(f)

#finds all crypto names
cryptoName = san.get("projects/all").slug


#get pandas df and merge dat
list_crypto = []
length = 0
start_date, stop_date = init_date()

#Stablecoins data:
#https://app.santiment.net/stablecoins#top-exchanges
#https://api.santiment.net/graphiql?query=%7B%0A%20%20allProjects%20%7B%0A%20%20%20%20slug%0A%20%20%20%20name%0A%20%20%20%20ticker%0A%20%20%20%20infrastructure%0A%20%20%20%20mainContractAddress%0A%20%20%7D%0A%7D%0A


stablecoins = ['tether',
               'binance-usd',
               'aave-busd',
               'aave-usdc',
               'compound-usd-coin',
               'p-usd-coin',
               'usdc-b',
               'usd-coin',
               'compound-dai',
               'dai',
               'multi-collateral-dai',
               'xdai',
               'terrausd',
               'trueusd',
               'paxos-standard',
               'liquity-usd',
               'frax',
               'neutrino-dollar',
               'fei-protocol',
               'husd',
               'gemini-dollar',
               'vai',
               'stasis-euro',
               'susd',
               'steem-dollars',
               'terra-krw',
               'empty-set-dollar',
               'anchor',
               'usdx-stablecoin',
               'bitcny',
               'just-stablecoin',
               'digix-gold-token',
               'eosdt',
               'cryptofranc',
               'basis-cash',
               'nubits',
               'stableusd',
               'dynamic-set-dollar',
               'midas-dollar',
               'tether-gold',
               'mith-cash',
               'one-cash',
               'brz',
               'augur']

total_length = len(cryptoName) - len(stablecoins)

#fetching each cryptocurrency
for crypto in cryptoName:
    if crypto not in stablecoins:
        print(f"{length} out of {total_length}")
        length += 1
        start_date_mod = start_date
        stop_date_mod = stop_date
        loop_number = 0
        dfAll = pd.DataFrame()
        lenDf = 1000

        #bypass limit
        while(1000 == lenDf):
            start_date_mod, stop_date_mod = init_date(days_delta = loop_number*1000)
            df = getDf(f'{crypto}', start_date_mod, stop_date_mod)
            lenDf = len(df)
            if lenDf > 0:
                dfAll = dfAll.append(df)
            loop_number += 1

        list_crypto.append(crypto)
        dfAll.sort_index(inplace=True)
        if len(dfAll) > 0:
            dfAll.to_pickle(f"data/raw/{crypto}.pkl")
            print(f"Successfully stored {crypto}")


with open("data/raw/crypto_list.dat", "wb") as f: #save list of cryptos selected as an object
    pickle.dump(list_crypto, f)
