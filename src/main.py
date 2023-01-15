from tqdm import tqdm
from dotenv import load_dotenv
import json
import requests
import os
import sqlite3

load_dotenv()
API_KEY = os.getenv("API_KEY")


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


def _load_data(
    company: str, statement_type: str, data_dirname: str = "data"
) -> list[dict[str, int | str]]:
    """
    Loads data from local json file and returns a dictionary
    """
    filepath = os.path.join(data_dirname, f"{statement_type}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return data[company]


def _fetch_data(company: str, statement_type: str) -> list[dict[str, int | str]]:
    """
    Fetches data from the API and returns a dictionary
    """
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{company}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


def _save_to_db(
    data: dict,
    statement_type: str,
    db_path: str = "/Users/lawrencelim/Projects/python-projects/pyfinny/financial_data.db",
):

    # Create a hashmap of the statement types
    name_map = {
        "balance-sheet-statement": "balance_sheet",
        "cash-flow-statement": "cash_flow_statement",
        "income-statement": "income_statement",
        "quote": "quote",
    }

    # Create data tuple and VALUES string
    data_tuple = tuple(data.values())
    values = "(" + "?, " * (len(data) - 1) + "?)"

    # Insert data into database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO {name_map[statement_type]} VALUES {values}", data_tuple
    )
    conn.commit()


def get_financials(
    companies: list[str],
    statement_types: list[str] = [
        "balance-sheet-statement",
        "cash-flow-statement",
        "income-statement",
        "quote",
    ],
) -> None:
    """
    Fetches data with API and writes to local sqlite3 database
    """
    for statement_type in statement_types:
        for company in tqdm(companies, desc=f"Updating {statement_type} file"):
            # financial_statement = _fetch_data(company, statement_type)
            financial_statement_data = _load_data(company, statement_type)
            for year_index in range(len(financial_statement_data)):
                _save_to_db(financial_statement_data[year_index], statement_type)


def main():
    companies = get_company_tickers()
    get_financials(companies)


if __name__ == "__main__":
    main()
