import os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

import sys
sys.path.append(parentdir)
import config as c

print("=== CONFIGURATION PARAMETERS ===")
print(f"Market cap: {c.market_cap}")
print(f"Expanding Windows: {c.windows}")
print(f"Number of cryptos: {c.number_cryptos}")
print("======================")
