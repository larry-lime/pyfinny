from tqdm import tqdm
from dotenv import load_dotenv
import json
import requests
import os

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
) -> dict[str,int|str]:
    """
    Returns a dictionary of financials for a given company and statement type
    """
    filepath = os.path.join(data_dirname, f"{statement_type}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return data[company]


def _fetch_data(company: str, statement_type: str) -> dict:
    """
    Returns a dictionary of financials for a given company and statement type
    """
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{company}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


def get_financials(
    companies: list[str], statement_types: list[str], data_dirname: str = "data"
) -> None:
    """
    Saves the data to a json file
    """
    for statement_type in statement_types:
        financial_statment = {}
        for company in tqdm(companies, desc=f"Updating {statement_type} file"):
            financial_statment[company] = _get_data(company, statement_type)
        json_object = json.dumps(financial_statment, indent=4)

        filepath = os.path.join(data_dirname, f"{statement_type}.json")
        with open(filepath, "w") as outfile:
            outfile.write(json_object)


def main():
    statement_types = [
        "income-statement",
        "cash-flow-statement",
        "balance-sheet-statement",
        "quote",
    ]
    companies = get_company_tickers()
    get_financials(companies, statement_types)


if __name__ == "__main__":
    main()
