# Python Financial Analyser Planning Doc

## Data Importer
- [ ]  Use API calls to import data from web resources
- [ ]  Save company financial statement data
- [ ]  Save company statistic data

## Comparables Analysis
- [ ]  Conduct comparable analysis with company statistics
- [ ]  Save the info as an excel file

## DCF Calculator
- [ ] Iteratively calculate a discounted cash flow model for numerous companies 
- [ ] Format the results nicely in an excel file 

## TODO List

### UI/UX
  - [ ] Allow users to delete wrong entries when entering in companies to load
  - [ ] 
  - [ ] 
### Comparables Analysis
  - [ ] Get the share price and add it to company statistics

### DCF Analysis

### Other
- [ ] Switch the API from the yahoo finance API to the financial modeling prep API
- [X] Fix the bug that read the wrong file name
- [ ] Look into using Finviz finance

## General

### Menu Tree
├── 1. Load Companies
│  ├── 1. Manually input ticker symbols
│  ├── 2. Read ticker symbols from tickers.csv
│  ├── 3. 
│  ├──  AAPL_financials_binary
│  ├──  AAPL_stats.csv
│  ├──  AAPL_stats.txt
│  ├──  AAPL_stats_binary
│  ├──  AAPL_wacc.csv
│  └──  AAPL_wacc.txt
├── 2. Compare Companies
│  ├──  GOOG_fin.csv
│  ├──  GOOG_fin.txt
│  ├──  GOOG_fin.xlsx
│  ├──  GOOG_financials_binary
│  ├──  GOOG_stats.csv
│  ├──  GOOG_stats.txt
│  ├──  GOOG_stats_binary
│  ├──  GOOG_wacc.csv
│  └──  GOOG_wacc.txt
└── 3. Exit Program
