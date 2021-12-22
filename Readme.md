# Presentation of the project

This project has for goal to explore different quantitative strategies which have already been proved profitable in the equity market and apply them to the cryptocurrency industry. Our focus for this project is on the Low Beta Anomaly observed empirically on many asset classes. The program can be configured for a preferred number of cryptocurrencies in portfolios and different market capitalization thresholds.

This program includes a Dash dashboard which is launched at the end of the ./launch.sh file. The dashboard can then be opened on the following port: http://127.0.0.1:8050/.


## Instructions for running the project

1) Clone project

```bash
git clone
```

2) Go into project folder

```bash
cd path_you_saved_the_project_in/lowbeta_cryptocurrency
```

3) Create your virtual environment (optional)

```bash
python3 -m venv venv
```

4) Enter in your virtual environment (optional)

* Mac OS / linux
```bash
source venv/bin/activate venv venv
```

* Windows
```bash
.\venv\Scripts\activate
```

5) Install libraries

* Python 3
```bash
pip3 install -r requirements.txt
```

5) select the environment variable in the config.py file

6) run the project

```bash
./launch.sh
```

### Run the dashboard only

```bash
python3 dashboard.py
```

# Project structure

```
├── data
│   ├── processed      <- The final, canonical data sets for modelling.
│   ├── strats         <- Data Results of our different strategies
│   └── raw            <- The original, immutable data dump.
│
├── graphs             <- All of the graphical files created by the graph_maker.py are stored here
│
│
├── latex              <- latex tables and files for our report are stored here                    
│
├── notebooks          <- Jupyter notebooks for data testing and visualization
│
├── old                <- Previous scripts which have been updated in the project
│
│
├── preprocessing/     <- Data cleaning and preprocessing scripts are here
│   │
│   ├── close_marketcap_merger.py    <- Merges individual crypto files to marketcap and close prices
│   │
│   ├── crypto_selector.py           <- Finds the first date of appearance of cryptos and marketcap threshold limit          
│   │
│   ├── returns_maker.py             <- Generates a cleaned dataframe of returns
│
│  
├── strats/            <- Strategy implementations are done here
│   │
│   ├── BTC.py                       <- Bitcoin performance script
│   │
│   ├── CW.py                        <- Capitalization Weighted portfolio performance script      
│   │
│   ├── EW.py                        <- Equally Weighted portfolio performance script
│   │
│   ├── functions.py                 <- Helper functions such as turnover and different rebalancement calculations        
│   │
│   ├── low_beta_BTC.py              <- Low Beta portfolio with Bitcoin as benchmark performance script
│   │
│   ├── low_beta_EW.py               <- Low Beta portfolio with Equally Weighted portfolio as benchmark performance script         
│   │
│   ├── low_beta.py                  <- Low Beta portfolio with Capitalization Weighted portfolio as benchmark performance script
│   │
│   ├── low_vol_split.py             <- Low Volatility portfolio performance script with data split for the existence of leverage
│   │
│   ├── low_vol.py                   <- Low Volatility portfolio performance script     
│   │
│   ├── MV.py                        <- Minimum Variance portfolio performance script   
│   │
│   ├── show_parameters.py           <- Script to show the configuration parameters when running the program
│  
├── config.py          <- Configuration files for environment variable selection
│   
├── dashboard.py       <- Dashboard launch script
│
├── launch.sh          <- Shell file to launch the whole program at once
│
├── makefile.py        <- Makefile to launch different parts of the code separately
│
├── metrics_maker.py   <- Script for metrics creation
│
├── Readme.md          <- Readme file for information about the project
│
│
├── requirements.txt   <- List of all Python modules required to launch the program
│
├── scrapper.py        <- Raw file script fetching individual cryptocurrency data from Santiment
│                         
```


## Ideas

- Li et Yi, Toward a Factor Structure in Crypto Asset Returns => seems to have a low vol anomaly
- https://coinmarketexpert.com/how-we-developed-a-cryptocurrency-portfolio-that-beats-bitcoin/
- https://www.econstor.eu/bitstream/10419/158007/1/887992064.pdf
- https://www.solactive.com/wp-content/uploads/2019/04/Solactive-Index-Guideline-CMC200.pdf
- https://iranarze.ir/wp-content/uploads/2021/01/11310-English-IranArze.pdf
- https://www.sciencedirect.com/science/article/pii/S2405844021022714 (Factor investing: A stock selection methodology for the European equity market)
- https://dune.xyz/rchen8/defi-users-over-time, for choosing the low vol split
- https://brightnode.io/history-of-makerdao-project/, history of makerdao
- https://compound.finance/documents/Compound.Whitepaper.pdf, compound whitepaper



## Authors

* Dimitri André : dimitri.andre@unil.ch
* Ruben Kempter : ruben.kempter@unil.ch
* Nicolas Eon Duval : nicolas.eonduval@unil.ch
* Guillaume Pavé : guillaume.pave@unil.ch
