from tqdm import tqdm
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")

# TODO: move this to a separate file
companies = [
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOG",
]

statement_types = [
    "income-statement",
    "cash-flow-statement",
    "balance-sheet-statement",
    "quote",
]


def get_financials(company: str, statement_type: str) -> dict:
    """
    Returns a dictionary of financials for a given company and statement type
    """
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{company}?apikey={API_KEY}"
    response = requests.get(url)  # GET request
    data = response.json()
    return data


def get_company_tickers(
    filename: str = "companies.txt", ticker_dirname: str = "tickers"
) -> list[str]:
    """
    Reads a file of tickers and returns a list of tickers
    """
    companies = []
    filepath = os.path.join(ticker_dirname, filename)
    with open(filepath, "r") as f:
        for line in f:
            companies.append(line.strip())
    return companies


def save_data(
    companies: list[str], statement_types: list[str], data_dirname: str = "data"
) -> None:
    """
    Saves the data to a json file
    """
    for statement_type in statement_types:
        financial_statment = {}
        for company in tqdm(companies, desc=f"Updating {statement_type} file"):
            financial_statment[company] = get_financials(company, statement_type)
        json_object = json.dumps(financial_statment, indent=4)

        filepath = os.path.join(data_dirname, f"{statement_type}.json")
        with open(filepath, "w") as outfile:
            outfile.write(json_object)


def main():
    print(get_company_tickers())


if __name__ == "__main__":
    main()
    # test(companies,statement_types)
