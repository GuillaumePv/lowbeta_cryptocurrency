#!/bin/bash
cd preprocessing
python3 close_marketcap_merger.py
python3 crypto_selector.py
python3 returns_maker.py
cd ..
cd strats
python3 show_parameters.py
python3 CW.py
python3 EW.py
python3 MV.py
python3 low_beta.py
python3 low_beta_EW.py
python3 low_vol.py
cd ..
python3 metrics_maker.py
python3 dashboard.py
