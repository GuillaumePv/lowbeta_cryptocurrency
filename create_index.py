import pandas as pd
import os
from tqdm import tqdm

df = pd.read_csv("./data/processed/market_cap_crypto.csv", index_col=0)
data = {}

# Cap_weigthed index
# for column in df.columns[:]:
#     data[column] = df[column]/df['total_market_cap']
# df_weight = pd.DataFrame(data)
# df_weight.to_csv('./data/processed/weights_cap_weigthed_index.csv', index=True)


#ponderate_index
print(df.count(axis='columns'))
