## To-do

- [x] scrap data
- [ ] read articles about low-beta and low-vol
- [x] create overleaf
- [ ] do planning
- [x] ERC / ...
- [x] process data
- [ ] split code for each strategies (Dimitri)
- [ ] create dashboard (Nico)
- [x] make minimum variance portfolio
- [ ] order first date
- [ ] create a excess return
- [ ] create % of reduction of portfolio compared to index
- [x] debug optimizer
- [ ] do algo market cap selection (1$ mio)

## Ideas
- low beta => buy low beta and sell high beta
- low vol => buy low vol and sell high beta
- use volume to create index
- dashboard: https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-financial-report
- https://stackoverflow.com/questions/58749930/low-volatility-portfolio-construction
- rolling covariance: https://stackoverflow.com/questions/45062622/create-rolling-covariance-matrix-in-pandas

Examples of dashboard:
https://github.com/plotly/dash-sample-apps/tree/main/apps

https://fr.tradingview.com/markets/cryptocurrencies/global-charts/

Examples of github: https://github.com/sakex/qarmII

- first code => monacoin bug

## Bibliography

- Li et Yi, Toward a Factor Structure in Crypto Asset Returns => seems to have a low vol anomaly

## Articles

- https://coinmarketexpert.com/how-we-developed-a-cryptocurrency-portfolio-that-beats-bitcoin/
- https://www.econstor.eu/bitstream/10419/158007/1/887992064.pdf
- https://www.solactive.com/wp-content/uploads/2019/04/Solactive-Index-Guideline-CMC200.pdf

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
