import os
import sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
import config as c

print("=== our parameters ===")
print(f"Market cap: {c.market_cap}")
print(f"Expanding Windows: {c.windows}")
print(f"Number of cryptos: {c.number_cryptos}")
print(f"Rebalancing: {c.rebalancing}")
print("======================")