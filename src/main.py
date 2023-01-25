from tqdm import tqdm
from dotenv import load_dotenv
import json
import requests
import os
import sqlite3
import openpyxl

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Directory Names
resource_dirname = "resources"
data_dirname = "data"

statement_types = [
    "balance-sheet-statement",
    "cash-flow-statement",
    "income-statement",
    "profile",
]


def get_company_tickers(
    filename: str = "load.txt",
    ticker_dirname: str = "tickers",
) -> list[str]:
    """
    Reads a file of tickers and returns a list of tickers
    """
    companies = []
    filepath = os.path.join(ticker_dirname, filename)
    with open(filepath, "r") as f:
        companies.extend(line.strip() for line in f)
    return companies


def _load_from_json(company: str, statement_type: str) -> list[dict[str, int | str]]:
    """
    Loads data from local json file and returns a dictionary
    """
    filepath = os.path.join(data_dirname, f"{statement_type}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return data[company]


def _fetch_from_api(company: str, statement_type: str) -> list[dict[str, int | str]]:
    """
    Fetches data from the API and returns a dictionary
    """
    # NOTE Limit is set to 4 because we only want the last 4 years of data
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{company}?apikey={API_KEY}&limit=4"
    response = requests.get(url)
    return response.json()


def _save_to_db(
    data: dict,
    statement_type: str,
    db_path: str = "financial_data.db",
):
    """
    Writes data to sqlite3 database
    """

    # Create a hashmap of the statement types
    name_map = {
        "balance-sheet-statement": "balance_sheet",
        "cash-flow-statement": "cash_flow_statement",
        "income-statement": "income_statement",
        "profile": "profile",
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
) -> None:
    """
    Calls _fetch_from_api() to fetch data from the API and _save_to_db() to save the data to a database
    """
    for statement_type in statement_types:
        for company in tqdm(companies, desc=f"Writing {statement_type} data"):
            financial_statement_data = _fetch_from_api(company, statement_type)
            # financial_statement_data = _load_from_json(company, statement_type)
            for year_index in range(len(financial_statement_data)):
                _save_to_db(financial_statement_data[year_index], statement_type)


def _comparables_analysis_helper(
    company: str,
    db_path: str = "financial_data.db",
) -> tuple:
    """
    Writes data from sqlite3 database to xlsx file
    """

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    profile_dict = {
        "price": 0.0,
        "mktCap": 0,
    }
    income_statement_dict = {
        "netIncome": 0,
        "revenue": 0,
        "ebitda": 0,
        "depreciationAndAmortization": 0,
    }
    balance_sheet_dict = {
        "cashAndCashEquivalents": 0,
        "totalDebt": 0,
    }
    cash_flow_statement_dict = {}

    # Fetch corresponding data from database and add it to the dictionary
    for value_type in profile_dict:
        cursor.execute(f"SELECT {value_type} FROM profile WHERE symbol = '{company}'")
        profile_dict[value_type] = cursor.fetchone()[0]
    for value_type in income_statement_dict:
        cursor.execute(
            f"SELECT {value_type} FROM income_statement WHERE symbol = '{company}'"
        )
        income_statement_dict[value_type] = cursor.fetchone()[0]
    for value_type in balance_sheet_dict:
        cursor.execute(
            f"SELECT {value_type} FROM balance_sheet WHERE symbol = '{company}'"
        )
        balance_sheet_dict[value_type] = cursor.fetchone()[0]
    for value_type in cash_flow_statement_dict:
        cursor.execute(
            f"SELECT {value_type} FROM cash_flow_statement WHERE symbol = {company}"
        )
        cash_flow_statement_dict[value_type] = cursor.fetchone()[0]

    return (
        profile_dict,
        income_statement_dict,
        balance_sheet_dict,
        cash_flow_statement_dict,
    )


def comparables_analysis(
    companies: list[str],
    template_name: str = "Template",
    comparables_analysis_name: str = "comparables_analysis.xlsx",
) -> None:
    """
    Writes data from sqlite3 database to comparables_analysis.xlsx
    """
    # Open xlsx file
    comparables_analysis_path = os.path.join(
        resource_dirname, comparables_analysis_name
    )
    workbook = openpyxl.load_workbook(comparables_analysis_path)
    # Make a copy of the first sheet
    workbook.copy_worksheet(workbook[template_name])

    # Rename the worksheet
    worksheet = workbook["Template Copy"]
    worksheet.title = " ".join(companies)

    # Change active worksheet
    workbook.active = worksheet

    starting_row = 7
    unit = 1000000

    for row_increment, company in enumerate(companies):
        (
            profile_dict,
            income_statement_dict,
            balance_sheet_dict,
            cash_flow_statement_dict,
        ) = _comparables_analysis_helper(company)

        price = profile_dict["price"]
        marketCap = profile_dict["mktCap"]
        ev = (
            marketCap
            + balance_sheet_dict["totalDebt"]
            - balance_sheet_dict["cashAndCashEquivalents"]
        )
        ebitda = income_statement_dict["ebitda"]
        ebit = ebitda - income_statement_dict["depreciationAndAmortization"]
        revenue = income_statement_dict["revenue"]
        earnings = income_statement_dict["netIncome"]

        # Insert a row
        worksheet[f"B{starting_row}"] = company
        worksheet[f"C{starting_row}"] = price
        worksheet[f"D{starting_row}"] = marketCap // unit
        worksheet[f"E{starting_row}"] = ev // unit
        worksheet[f"F{starting_row}"] = revenue // unit
        worksheet[f"G{starting_row}"] = ebitda // unit
        worksheet[f"H{starting_row}"] = ebit // unit
        worksheet[f"I{starting_row}"] = earnings // unit
        worksheet[
            f"J{starting_row}"
        ] = "=INDIRECT(ADDRESS(ROW(),COLUMN()-5))/INDIRECT(ADDRESS(ROW(),COLUMN()-4))"
        worksheet[
            f"K{starting_row}"
        ] = "=INDIRECT(ADDRESS(ROW(),COLUMN()-6))/INDIRECT(ADDRESS(ROW(),COLUMN()-4))"
        worksheet[
            f"L{starting_row}"
        ] = "=INDIRECT(ADDRESS(ROW(),COLUMN()-7))/INDIRECT(ADDRESS(ROW(),COLUMN()-4))"
        worksheet[
            f"M{starting_row}"
        ] = "=INDIRECT(ADDRESS(ROW(),COLUMN()-9))/INDIRECT(ADDRESS(ROW(),COLUMN()-4))"

        if row_increment < len(companies) - 1:
            workbook.active.insert_rows(starting_row)

    workbook.save(comparables_analysis_path)


# Combine this and _comparables_analysis_helper into one function
def _dcf_helper(
    company: str,
    db_path: str = "financial_data.db",
):

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Some Notes
    # Manually input perpetual growth
    # Calculate growth rate from the previous year's revenue
    # Get revenue for 4 years
    # Manually input risk free rate
    # Manually input expected return
    # Manually input Beta
    # effectiveTaxRate = incomeTaxExpense / incomeBeforeTax
    # Calculate NOPLAT from ebit * (1 - effectiveTaxRate)
    # Calculate average rate of debt
    profile_dict = {
        "price": 0.0,
        "mktCap": 0,
        "beta": 0.0,
    }
    income_statement_dict = {
        "netIncome": [],
        "revenue": [],
        "ebitda": [],
        "depreciationAndAmortization": [],
        "incomeTaxExpense": 0,
        "incomeBeforeTax": 0,
        "interestExpense": 0,
    }
    balance_sheet_dict = {
        "cashAndCashEquivalents": [],
        "totalCurrentAssets": [],
        "totalCurrentLiabilities": [],
        "totalDebt": 0,
    }
    cash_flow_statement_dict = {
        "capitalExpenditure": [],
    }

    # Values that need to be returned as a list because I need to do a three year projection
    # NOPLAT = ebit * (1 - (incomeTaxExpense / incomeBeforeTax))
    # workingCapital = totalCurrentAssets - totalCurrentLiabilities
    # average_rate_of_debt = (interestExpense / totalDebt) * -1
    # netIncome, NOPLAT, depreciationAndAmortization, workingCapital, capitalExpenditure

    # Values that are an integer or float. I have to figure out how to get beta though
    # sharesOutstanding, price, totalDebt, (latest) effectiveTaxRate

    for value_type in profile_dict:
        cursor.execute(f"SELECT {value_type} FROM profile WHERE symbol = '{company}'")
        profile_dict[value_type] = cursor.fetchone()[0]

    for value_type in income_statement_dict:
        cursor.execute(
            f"SELECT {value_type} FROM income_statement WHERE symbol = '{company}'"
        )
        if value_type in ["incomeTaxExpense", "incomeBeforeTax", "interestExpense"]:
            income_statement_dict[value_type] = cursor.fetchone()[0]
        else:
            income_statement_dict[value_type] = [tup[0] for tup in cursor.fetchall()]
    for value_type in balance_sheet_dict:
        cursor.execute(
            f"SELECT {value_type} FROM balance_sheet WHERE symbol = '{company}'"
        )
        if value_type in ["totalDebt"]:
            balance_sheet_dict[value_type] = cursor.fetchone()[0]
        else:
            balance_sheet_dict[value_type] = [tup[0] for tup in cursor.fetchall()]
    for value_type in cash_flow_statement_dict:
        cursor.execute(
            f"SELECT {value_type} FROM cash_flow_statement WHERE symbol = '{company}'"
        )
        cash_flow_statement_dict[value_type] = [tup[0] for tup in cursor.fetchall()]

    return (
        profile_dict,
        income_statement_dict,
        balance_sheet_dict,
        cash_flow_statement_dict,
    )


def dcf_analysis(
    companies: list[str],
    template_name: str = "Template",
    dcf_analysis_name: str = "dcf.xlsx",
):
    """
    Write a DCF analysis to an Excel file.
    """
    # Open xlsx file
    dcf_analysis_path = os.path.join(resource_dirname, dcf_analysis_name)
    workbook = openpyxl.load_workbook(dcf_analysis_path)

    # TODO: Complete the rest of the code here
    for company in companies:
        # Make a copy of the first sheet
        workbook.copy_worksheet(workbook[template_name])

        # Rename the worksheet
        worksheet = workbook["Template Copy"]
        worksheet.title = "".join(company)
        (
            profile_dict,
            income_statement_dict,
            balance_sheet_dict,
            cash_flow_statement_dict,
        ) = _dcf_helper(company)

        # DCF Valuation
        sharesOutstanding = profile_dict["mktCap"] / profile_dict["price"]
        current_share_price = profile_dict["price"]

        # FCF Buildup
        total_revenue = income_statement_dict["revenue"]
        netIncome = income_statement_dict["netIncome"]
        # NOTE: This changes when the range of years the DCF uses changes
        first_year_growth_rate = (total_revenue[1] - total_revenue[0]) / total_revenue[0]

        ebitda = income_statement_dict["ebitda"]
        depreciationAndAmortization = income_statement_dict[
            "depreciationAndAmortization"
        ]
        ebit = [e - d_and_a for e, d_and_a in zip(ebitda, depreciationAndAmortization)]
        effectiveTaxRate = (
            income_statement_dict["incomeTaxExpense"]
            / income_statement_dict["incomeBeforeTax"]
        )
        noplat = [e * (1 - effectiveTaxRate) for e in ebit]
        workingCapital = [
            tca - tcl
            for tca, tcl in zip(
                balance_sheet_dict["totalCurrentAssets"],
                balance_sheet_dict["totalCurrentLiabilities"],
            )
        ]
        capitalExpenditure = cash_flow_statement_dict["capitalExpenditure"]

        # WACC Calculation
        average_rate_of_debt = (
            income_statement_dict["interestExpense"] / balance_sheet_dict["totalDebt"]
        ) * -1
        tax_rate = effectiveTaxRate
        totalDebt = balance_sheet_dict["totalDebt"]
        marketCap = profile_dict["mktCap"]
        beta = profile_dict["beta"]

        # DCF Valuation
        # In C10, insert the number of shares outstanding
        worksheet["C10"] = sharesOutstanding
        # In C11, insert the current share price
        worksheet["C11"] = current_share_price

        # FCF Buildup
        # In C19, D19, E19, insert the total revenue for the last 3 years
        # Iterate over the last three values in the total_revenue list
        letters = ["C", "D", "E"]
        for revenue, letter in zip(total_revenue[-3:], letters):
            worksheet[f"{letter}19"] = revenue
        # In C19, insert the first year growth rate
        worksheet["C20"] = first_year_growth_rate
        # In C21, D21, E21, insert the net income for the last 3 years
        # Iterate over the last three values in the netIncome list
        for net_income, letter in zip(netIncome[-3:], letters):
            worksheet[f"{letter}21"] = net_income
        # In C24, D24, E24, insert the noplat for the last 3 years
        # Iterate over the last three values in the noplat list
        for noplat, letter in zip(noplat[-3:], letters):
            worksheet[f"{letter}24"] = noplat
        # In C26, D26, E26, insert the depreciationAndAmortization for the last 3 years
        # Iterate over the last three values in the depreciationAndAmortization list
        for dep_and_amort, letter in zip(depreciationAndAmortization[-3:], letters):
            worksheet[f"{letter}26"] = dep_and_amort
        # In C28, D28, E28, insert the workingCapital for the last 3 years
        # Iterate over the last three values in the workingCapital list
        for wc, letter in zip(workingCapital[-3:], letters):
            worksheet[f"{letter}28"] = wc
        # In C30, D30, E30, insert the capitalExpenditure for the last 3 years
        # Iterate over the last three values in the capitalExpenditure list
        for cap_expend, letter in zip(capitalExpenditure[-3:], letters):
            worksheet[f"{letter}30"] = cap_expend

        # WACC Calculation
        # In C36, insert the average_rate_of_debt
        worksheet["C36"] = average_rate_of_debt
        # In C37, insert the tax_rate
        worksheet["C37"] = tax_rate
        # In C40, insert the beta
        worksheet["C40"] = beta
        # In E36, insert the totalDebt
        worksheet["E36"] = totalDebt
        # In E37 insert the mkCap
        worksheet["E37"] = marketCap

    workbook.save(dcf_analysis_path)


def main():
    companies = get_company_tickers()
    # comparables_analysis(companies)
    dcf_analysis(companies)
    # (
    #     profile_dict,
    #     income_statement_dict,
    #     balance_sheet_dict,
    #     cash_flow_statement_dict,
    # ) = _dcf_helper("AAPL")
    # print("profile_dict")
    # [print(i, j) for i, j in profile_dict.items()]
    # print("\nincome_statement_dict")
    # [print(i, j) for i, j in income_statement_dict.items()]
    # print("\nbalance_sheet_dict")
    # [print(i, j) for i, j in balance_sheet_dict.items()]
    # print("\ncash_flow_statement_dict")
    # [print(i, j) for i, j in cash_flow_statement_dict.items()]
    # print(income_statement_dict)
    # print(balance_sheet_dict)
    # print(cash_flow_statement_dict)


if __name__ == "__main__":
    main()
