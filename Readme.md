# Presentation Project

Low Beta / low vol strategies in crypto market

## Ideas
- low beta => buy low beta and sell high beta
- low vol => buy low vol and sell high vol
- use volume to create index
- dashboard: https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-financial-report
- https://stackoverflow.com/questions/58749930/low-volatility-portfolio-construction
- rolling covariance: https://stackoverflow.com/questions/45062622/create-rolling-covariance-matrix-in-pandas
- crete dataset to run regression in stata

Examples of dashboard:
https://github.com/plotly/dash-sample-apps/tree/main/apps

https://fr.tradingview.com/markets/cryptocurrencies/global-charts/

Examples of github: 
- https://github.com/sakex/qarmII
- https://github.com/maxrel95/QARMII_TrendFollowing/blob/master/TrendFollowing_Topic15.pdf

## Data & Methodlogy

- returns are computed with logarithmic first difference
- we select cryptocurrencies based on their past 3, 6, 9, and 12 month volatility (voir avec le nombre de jour)

## Bibliography

- Li et Yi, Toward a Factor Structure in Crypto Asset Returns => seems to have a low vol anomaly

## Articles

- https://coinmarketexpert.com/how-we-developed-a-cryptocurrency-portfolio-that-beats-bitcoin/
- https://www.econstor.eu/bitstream/10419/158007/1/887992064.pdf
- https://www.solactive.com/wp-content/uploads/2019/04/Solactive-Index-Guideline-CMC200.pdf
- https://iranarze.ir/wp-content/uploads/2021/01/11310-English-IranArze.pdf

## Questions

- besoin d'un MRC, min variance ?
- how to compute vol ? daily ? Monthly ? (14 day / Monthly / Annual) => depend on the universe

## Indicators
- Beta
- Max drawdown
- Hit ratio
- Skewness
- Kurtosis
- Sharpe Ratio
