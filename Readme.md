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

## Data & Methodology

- returns are computed with logarithmic first difference
- we select cryptocurrencies based on their past 3, 6, 9, and 12 month volatility (voir avec le nombre de jour)
- Moreover, since it is possible to trade cryptos every day of the week, N
amounts to 7.

# Presentation of the project

Low Beta / low vol strategies in crypto market

## Abstract

## Authors

* Ruben Kempter : ruben.kempter@unil.ch
* Dimitri André : dimitri.andre@unil.ch
* Nicolas Eon Duval : nicolas.eonduval@unil.ch
* Guillaume Pavé : guillaume.pave@unil.ch

## Install libraries and run project

1) Clone project

```bash
git clone
```

2) Go into project folder

```bash
cd
```

3) Create your virtual environment

```bash
python3 -m venv venv
```

4) Enter in your virtual environment

* Mac OS / linux
```bash
source venv/bin/activate venv venv
```

* Windows
```bash
.\venv\Scripts\activate
```

5) Install libraries

* Python 2
```bash
pip install -r requirements.txt
```

* Python 3
```bash
pip3 install -r requirements.txt
```

6) using our makefile to run our project

* see helper of the makefile
```bash
make
```
# Project structure

In construction
```
├── README.md          <- The top-level README for developers using this project.
│
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   ├── strats         <- Data Results of our different strategies
│   └── raw            <- The original, immutable data dump.
│
├── latex /            <- latex files                     
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
│
│
├── plots /            <- static files (images)
│
│
├── preprocessing/   <- ML models used in the dasboard are stocked in this folder
│   │
│   ├── fetchScripts           <- Scripts to download or generate data
│
│  
├── strats/   <- ML models used in the dasboard are stocked in this folder
│   │
│   ├── fetchScripts           <- Scripts to download or generate data
│
│  
├── config.py   <- Main python file that manage all our different codes
│   
├── dashboard.py   <- Main python file that manage all our different codes
│
│
├── metrics_maker.py   <- Main python file that manage all our different codes
│
├── scrapper.py   <- Main python file that manage all our different codes
│
│
├── makefile   <- makefile to run project or each part of project
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
```

## Bibliography

- Li et Yi, Toward a Factor Structure in Crypto Asset Returns => seems to have a low vol anomaly

## Articles

- https://coinmarketexpert.com/how-we-developed-a-cryptocurrency-portfolio-that-beats-bitcoin/
- https://www.econstor.eu/bitstream/10419/158007/1/887992064.pdf
- https://www.solactive.com/wp-content/uploads/2019/04/Solactive-Index-Guideline-CMC200.pdf
- https://iranarze.ir/wp-content/uploads/2021/01/11310-English-IranArze.pdf
- https://www.sciencedirect.com/science/article/pii/S2405844021022714 (Factor investing: A stock selection methodology for the European equity market)
- https://dune.xyz/rchen8/defi-users-over-time, for choosing the low vol split
- https://brightnode.io/history-of-makerdao-project/, history of makerdao
- https://compound.finance/documents/Compound.Whitepaper.pdf, compound whitepaper

## Indicators
- Beta
- Max drawdown
- Hit ratio
- Skewness
- Kurtosis
- Sharpe Ratio
- Excess return

## Graphs to do in latex

- [ ] Bitcoin prevalence on Cap-weighted
- [ ] Tables of metrics for every rebalancement
- [ ] Graphs of perfs 20 and 100
- [ ] leverage split table low vol high vol
- [ ] Table of Sharpe taking into account turnover at 0.3% per trans
- [ ] Graph vola CW and ?
