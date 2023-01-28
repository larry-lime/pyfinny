# Pyfinny

## Introduction
This is a command-line interface (CLI) tool for analyzing financial statements and performing discounted cash flow (DCF) and comparables analysis. The tool uses the Financial Modelling Prep API, which requires an API key. The Github repository with source code and release binaries can be found [here](https://github.com/larry-lime/pyfinny)

## Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Optional Requirements](#optional-requirements)
4. [Installation](#installation)
5. [Usage](#usage)
    1. [Setup](#setup)
    2. [Open Excel File](#open-excel-file)
    3. [Load Company Financial Statements](#load-company-financial-statements)
    4. [Print Data from Database](#print-data-from-database)
    5. [Print Tickers](#print-tickers)
    6. [Discounted Cash Flow Analysis](#discounted-cash-flow-analysis)
    7. [Comparables Analysis](#comparables-analysis)

## Requirements
1. Python 3.10 installation
2. Account with [Financial Modeling Prep](https://site.financialmodelingprep.com/)
3. Bash or Zsh terminal. Windows users are highly advised to use WSL

## Optional Requirements
1. [Sqlite Browser](https://sqlitebrowser.org/) to view and manipulate the data in the database
2. [Homebrew](https://brew.sh/) and Git to develop the application

## Installation
Note: use `python3`,`pip3` on MacOS and `python`, `pip` on Windows
1. Clone the repository or download the [release binary](https://github.com/larry-lime/pyfinny/releases/download/v1.0.0/pyfinny-1.0.0.zip)
    ```shell
    git clone https://github.com/larry-lime/pyfinny.git
    cd pyfinny
    ```
2. Create and start python virtual environment
    ```shell
    python -m venv venv
    ```
3. Activate Python virtual environment
    ```shell
    source venv/bin/activate
    ```
4. Install requirements
    ```shell
    python3 setup.py develop
    ```
## Usage
Run `pyfin` in your terminal to begin using the application
### Setup

Before you begin analyzing, you must run the setup command to provide your Financial Modelling Prep API Key and create the necessary database.
```shell
pyfin setup
```

### Open Excel File

To open an Excel file, use the open command and provide the name of the file without the file extension. The `-d` or `--resource_dir` option can be used to specify the directory where the Excel file is located. If not provided, the default directory is `resources`.
```shell
pyfin open filename [-d|--resource_dir]
```
#### Examples
To open the DCF template, run the following command:
```shell
pyfin open dcf
```
To open the comparables analysis template, run the following command:
```shell
pyfin open compare
```

### Load Company Financial Statements

To load company financial statements, use the load command. The `-f` or `--filename` option can be used to specify the file containing the tickers of the companies to load. If not provided, the default file is `load.txt`.
```shell
pyfin load [-f|--filename]
```
#### Examples
To load the financial statements of the companies in `load.txt`, run the following command:
```shell
pyfin load
```
To load the financial statements of the companies in `dcf.txt`, run the following command:
```shell
pyfin load -f dcf.txt
```

### Print Data from Database

To print data from the database, use the data command. The `-t` or `--table` option can be used to specify the table to print. If this option is not provided, the user will be prompted to choose which tables to print.

```
pyfin data [-t|--table]
```
#### Examples
To start the interactive prompt, run the following command:
```shell
pyfin data
```

To print the data from the `income_statement` table, run the following command:
```shell
pyfin data -t income_statement
```

### Print Tickers

To print the tickers in a file, use the tickers command. The `-f` or `--filename` option can be used to specify the file containing the tickers. If not provided, the default file is `load.txt`. The `-d` or `--ticker_dir` option can be used to specify the directory where the ticker files are located. If not provided, the default directory is `tickers`.
```shell
pyfin tickers [-f|--filename] [-d|--ticker_dir]
```
#### Examples
To print the tickers in `load.txt`, run the following command:
```shell
pyfin tickers
```
To print the tickers in `dcf.txt`, run the following command:
```shell
pyfin tickers -f dcf.txt
```


### Discounted Cash Flow Analysis

To perform a discounted cash flow analysis, use the dcf command. The `-f` or `--filename` option can be used to specify the file containing the tickers to use for the analysis. If not provided, the default file is `load.txt`. The `-t` or `--template_name` option can be used to specify the name of the Excel sheet containing the DCF template. If not provided, the default sheet name is `Template`. The `-n` or `--dcf_analysis_name` option can be used to specify the name of the Excel file to write the DCF analysis to. If not provided, the default file name is `dcf.xlsx`.
```shell
pyfin dcf [-f|--filename] [-t|--template_name] [-n|--dcf_analysis_name]
```
#### Examples
To perform a DCF analysis using the companies in `dcf.txt`, run the following command:
```shell
pyfin dcf
```


### Comparables Analysis

To perform a comparables analysis, use the comparables command. The `-n` or `--comparables_analysis_name` option can be used to specify the name of the Excel file to write the comparables analysis to. If not provided, the default file name is `compare.xlsx`. The `-f` or `--filename` option can be used to specify the file containing the tickers to use for the analysis. If not provided, the default file is `load.txt`.

```shell
pyfin compare [-n|--comparables_analysis_name] [-f|--filename]
```
#### Examples
To perform a comparables analysis using the companies in `compare.txt`, run the following command:
```shell
pyfin compare
```

