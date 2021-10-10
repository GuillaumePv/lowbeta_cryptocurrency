#Basic Utilities
import pandas
from datetime import date, timedelta

#Data fetchers
import san

#################
#Functions
################

def getMarketcap(crypto="bitcoin"):
    mktcap = san.get(
        f"marketcap_usd/{crypto}",
        from_date=today,
        to_date=today
        )
    return mktcap.value[-1]


#################
#Script
#################

#finds all crypto names
#cryptoName = san.get("projects/all").name

#get date
today_raw = date.today()
today = today_raw.strftime("%Y-%m-%d")



"""
bite = san.get(
    "ohlc/santiment",
    from_date="2012-06-01",
    to_date="2020-06-05",
    interval="1d"
)

print(len(bite))
"""
