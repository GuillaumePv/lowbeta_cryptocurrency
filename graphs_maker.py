import pandas as pd
import numpy as np
from matplotlib import plt

#Bitcoin prevalence on Cap-weighted
plt.figure(figsize=(6.4 * 3, 4.8 *6))
plt.plot(X, Y)
plt.title(“title”)
plt.plot(X, y, ‘bo’, label = “legend”)
plt.savefig('output.jpeg')

#Tables of metrics for every rebalancement

#Graphs of perfs 20 and 100

#leverage split table low vol high vol

#Table of Sharpe taking into account turnover at 0.3% per trans

#Graph vola CW and ?
