# Presentation of the project

This project has for goal to explore different quantitative strategies which have already been proved profitable in the equity market and apply them to the cryptocurrency industry. Our focus for this project is on the Low Beta Anomaly observed empirically on many asset classes. The program can be configured for a preferred number of cryptocurrencies in portfolios and different market capitalization thresholds.

This program includes a Dash dashboard which is launched at the end of the ./launch.sh file. The dashboard can then be opened on the following port: http://127.0.0.1:8050/.


## Instructions for running the project

1) Clone project

```bash
git clone https://github.com/GuillaumePv/lowbeta_cryptocurrency.git
```

2) Go into project folder

```bash
cd lowbeta_cryptocurrency
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

6) Go to config.py in the project folder with your IDE and modify the environment variables (optional)

7) Run the project from the terminal

Go into the project folder and run the following command

```bash
./launch.sh
```
Open your browser and go to http://127.0.0.1:8050/

### Run the dashboard only

Go into the project folder and run the following command

```bash
python3 dashboard.py
```

Open your browser and go to http://127.0.0.1:8050/

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

## Authors

* Dimitri André : dimitri.andre@unil.ch
* Ruben Kempter : ruben.kempter@unil.ch
* Nicolas Eon Duval : nicolas.eonduval@unil.ch
* Guillaume Pavé : guillaume.pave@unil.ch
