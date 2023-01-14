# Pyfinny

## Installation
1. Clone the repository
    ```shell
    git clone https://github.com/larry-lime/pyfinny.git
    cd pyfinny
    ```
2. Create a python virtual environment
    ```shell
    python3 -m venv .
    ```
3. Activate Python virtual environment
    ```shell
    source bin/activate
    ```
4. Install requirements
    ```shell
    pip3 install -r requirements.txt
    ```

## Usage

### Comparable Analysis

#### Data Needed
- Total Assets
- Total Liabilities
- Market Cap
- Market Price
- Net Income
- Gross Profit
- Total Revenue
- EBIT
- P/E Ratio
- Div Yield


### Discounted Cash Flow Model

## Directory Structure
 src
├──  comparables
├──  scripts
│  ├──  __pycache__
│  │  ├──  analysis.cpython-310.pyc
│  │  ├──  compare.cpython-310.pyc
│  │  └──  utils.cpython-310.pyc
│  ├──  analysis.py
│  ├──  compare.py
│  ├──  error_log.txt
│  ├──  financials
│  ├──  start.py
│  ├──  temp.py
│  └──  utils.py
└──  tickers
   └──  sample_tickers.csv
