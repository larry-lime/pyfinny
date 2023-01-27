from tqdm import tqdm
import subprocess
from dotenv import load_dotenv
import json
import requests
import os
import sqlite3
import openpyxl
import platform

load_dotenv()
API_KEY = os.getenv("API_KEY")

resource_dirname = "resources"
unit = 1000000

statement_types = [
    "balance-sheet-statement",
    "cash-flow-statement",
    "income-statement",
    "profile",
]


def open_xlsx(
    resource_dirname: str = "resources",
    filename: str = "pyfinny.xlsx",
):
    """
    Open the excel file
    """
    filepath = os.path.join(resource_dirname, filename)
    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", filepath))
    elif platform.system() == "Windows":  # Windows
        os.open(filename, os.O_RDWR | os.O_CREAT)
    else:  # linux variants
        subprocess.call(("xdg-open", filename))

def get_tables():
    """
    Get the tables from the database
    """
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()

def show_data(table_name):
    """
    Display the data from the database
    """
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    # Format the data
    print(f"Table: {table_name}")
    print("---------------")
    for row in cursor.fetchall():
        print(row)
    print("---------------")



def set_api_key(
    apikey: str = "<API_KEY>",
):
    """
    Creates a .env file with the API key
    """
    with open(".env", "w") as f:
        f.write(f"API_KEY={apikey}")


def make_database(
    db_path: str = "financial_data.db",
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # If the table doesn't exist, create it
    cursor.execute(
        """
    CREATE TABLE "balance_sheet" (
	"date"	TEXT,
	"symbol"	TEXT,
	"reportedCurrency"	TEXT,
	"cik"	TEXT,
	"fillingDate"	TEXT,
	"acceptedDate"	TEXT,
	"calendarYear"	TEXT,
	"period"	TEXT,
	"cashAndCashEquivalents"	INTEGER,
	"shortTermInvestments"	INTEGER,
	"cashAndShortTermInvestments"	INTEGER,
	"netReceivables"	INTEGER,
	"inventory"	INTEGER,
	"otherCurrentAssets"	INTEGER,
	"totalCurrentAssets"	INTEGER,
	"propertyPlantEquipmentNet"	INTEGER,
	"goodwill"	REAL,
	"intangibleAssets"	REAL,
	"goodwillAndIntangibleAssets"	REAL,
	"longTermInvestments"	INTEGER,
	"taxAssets"	REAL,
	"otherNonCurrentAssets"	INTEGER,
	"totalNonCurrentAssets"	INTEGER,
	"otherAssets"	REAL,
	"totalAssets"	INTEGER,
	"accountPayables"	INTEGER,
	"shortTermDebt"	INTEGER,
	"taxPayables"	REAL,
	"deferredRevenue"	INTEGER,
	"otherCurrentLiabilities"	INTEGER,
	"totalCurrentLiabilities"	INTEGER,
	"longTermDebt"	INTEGER,
	"deferredRevenueNonCurrent"	REAL,
	"deferredTaxLiabilitiesNonCurrent"	REAL,
	"otherNonCurrentLiabilities"	INTEGER,
	"totalNonCurrentLiabilities"	INTEGER,
	"otherLiabilities"	REAL,
	"capitalLeaseObligations"	REAL,
	"totalLiabilities"	INTEGER,
	"preferredStock"	INTEGER,
	"commonStock"	INTEGER,
	"retainedEarnings"	INTEGER,
	"accumulatedOtherComprehensiveIncomeLoss"	INTEGER,
	"othertotalStockholdersEquity"	REAL,
	"totalStockholdersEquity"	INTEGER,
	"totalLiabilitiesAndStockholdersEquity"	INTEGER,
	"minorityInterest"	INTEGER,
	"totalEquity"	INTEGER,
	"totalLiabilitiesAndTotalEquity"	INTEGER,
	"totalInvestments"	INTEGER,
	"totalDebt"	INTEGER,
	"netDebt"	INTEGER,
	"link"	TEXT,
	"finalLink"	TEXT
);
            """
    )
    conn.execute(
        """
            CREATE TABLE "cash_flow_statement" (
	"date"	TEXT,
	"symbol"	TEXT,
	"reportedCurrency"	TEXT,
	"cik"	TEXT,
	"fillingDate"	TEXT,
	"acceptedDate"	TEXT,
	"calendarYear"	TEXT,
	"period"	TEXT,
	"netIncome"	INTEGER,
	"depreciationAndAmortization"	INTEGER,
	"deferredIncomeTax"	INTEGER,
	"stockBasedCompensation"	INTEGER,
	"changeInWorkingCapital"	INTEGER,
	"accountsReceivables"	INTEGER,
	"inventory"	INTEGER,
	"accountsPayables"	INTEGER,
	"otherWorkingCapital"	INTEGER,
	"otherNonCashItems"	INTEGER,
	"netCashProvidedByOperatingActivities"	INTEGER,
	"investmentsInPropertyPlantAndEquipment"	INTEGER,
	"acquisitionsNet"	INTEGER,
	"purchasesOfInvestments"	INTEGER,
	"salesMaturitiesOfInvestments"	INTEGER,
	"otherInvestingActivites"	INTEGER,
	"netCashUsedForInvestingActivites"	INTEGER,
	"debtRepayment"	INTEGER,
	"commonStockIssued"	INTEGER,
	"commonStockRepurchased"	INTEGER,
	"dividendsPaid"	INTEGER,
	"otherFinancingActivites"	INTEGER,
	"netCashUsedProvidedByFinancingActivities"	INTEGER,
	"effectOfForexChangesOnCash"	INTEGER,
	"netChangeInCash"	INTEGER,
	"cashAtEndOfPeriod"	INTEGER,
	"cashAtBeginningOfPeriod"	INTEGER,
	"operatingCashFlow"	INTEGER,
	"capitalExpenditure"	INTEGER,
	"freeCashFlow"	INTEGER,
	"link"	TEXT,
	"finalLink"	TEXT
);
            """
    )
    conn.execute(
        """
            CREATE TABLE "income_statement" (
	"date"	TEXT,
	"symbol"	TEXT,
	"reportedCurrency"	TEXT,
	"cik"	TEXT,
	"fillingDate"	TEXT,
	"acceptedDate"	TEXT,
	"calendarYear"	TEXT,
	"period"	TEXT,
	"revenue"	INTEGER,
	"costOfRevenue"	INTEGER,
	"grossProfit"	INTEGER,
	"grossProfitRatio"	REAL,
	"researchAndDevelopmentExpenses"	INTEGER,
	"generalAndAdministrativeExpenses"	INTEGER,
	"sellingAndMarketingExpenses"	INTEGER,
	"sellingGeneralAndAdministrativeExpenses"	INTEGER,
	"otherExpenses"	INTEGER,
	"operatingExpenses"	INTEGER,
	"costAndExpenses"	INTEGER,
	"interestIncome"	INTEGER,
	"interestExpense"	INTEGER,
	"depreciationAndAmortization"	INTEGER,
	"ebitda"	INTEGER,
	"ebitdaratio"	REAL,
	"operatingIncome"	INTEGER,
	"operatingIncomeRatio"	REAL,
	"totalOtherIncomeExpensesNet"	INTEGER,
	"incomeBeforeTax"	INTEGER,
	"incomeBeforeTaxRatio"	REAL,
	"incomeTaxExpense"	INTEGER,
	"netIncome"	INTEGER,
	"netIncomeRatio"	REAL,
	"eps"	REAL,
	"epsdiluted"	REAL,
	"weightedAverageShsOut"	INTEGER,
	"weightedAverageShsOutDil"	INTEGER,
	"link"	TEXT,
	"finalLink"	TEXT
);
            """
    )
    conn.execute(
        """
            CREATE TABLE "profile" (
	"symbol"	TEXT,
	"price"	REAL,
	"beta"	REAL,
	"volAvg"	INTEGER,
	"mktCap"	REAL,
	"lastDiv"	REAL,
	"range"	TEXT,
	"changes"	REAL,
	"companyName"	TEXT,
	"currency"	TEXT,
	"cik"	TEXT,
	"isin"	TEXT,
	"cusip"	TEXT,
	"exchange"	TEXT,
	"exchangeShortName"	TEXT,
	"industry"	TEXT,
	"website"	TEXT,
	"description"	TEXT,
	"ceo"	TEXT,
	"sector"	TEXT,
	"country"	TEXT,
	"fullTimeEmployees"	TEXT,
	"phone"	TEXT,
	"address"	TEXT,
	"city"	TEXT,
	"state"	TEXT,
	"zip"	TEXT,
	"dcfDiff"	REAL,
	"dcf"	REAL,
	"image"	TEXT,
	"ipoDate"	TEXT,
	"defaultImage"	BOOLEAN,
	"isEtf"	BOOLEAN,
	"isActivelyTrading"	BOOLEAN,
	"isAdr"	BOOLEAN,
	"isFund"	BOOLEAN
);
            """
    )
    conn.commit()


def get_financials(
    filename: str,
) -> None:
    """
    Calls _fetch_from_api() to fetch data from the API and _save_to_db() to save the data to a database
    """
    companies = get_company_tickers(filename)
    for statement_type in statement_types:
        for company in tqdm(companies, desc=f"Writing {statement_type} data"):
            financial_statement_data = fetch_from_api(company, statement_type)
            # financial_statement_data = _load_from_json(company, statement_type)
            for year_index in range(len(financial_statement_data)):
                save_to_db(financial_statement_data[year_index], statement_type)


def dcf_analysis(
    filename,
    template_name,
    dcf_analysis_name,
):  # sourcery skip: hoist-statement-from-loop
    """
    Write a DCF analysis to an Excel file.
    """
    # Open xlsx file
    dcf_analysis_path = os.path.join(resource_dirname, dcf_analysis_name)
    workbook = openpyxl.load_workbook(dcf_analysis_path)

    companies = get_company_tickers(filename)
    for company in companies:
        workbook.copy_worksheet(workbook[template_name])
        worksheet = workbook["Template Copy"]
        worksheet.title = "".join(company)
        (
            profile,
            income_statement,
            balance_sheet,
            cash_flow_statement,
        ) = _dcf_helper(company)

        # Load Data
        current_share_price = profile["price"]
        marketCap = profile["mktCap"]
        beta = profile["beta"]
        total_rev = income_statement["revenue"]
        netIncome = income_statement["netIncome"]
        ebitda = income_statement["ebitda"]
        depreciationAndAmortization = income_statement["depreciationAndAmortization"]
        totalDebt = balance_sheet["totalDebt"]
        capitalExpenditure = cash_flow_statement["capitalExpenditure"]

        # Calculate Additional Metrics
        first_year_growth_rate = (total_rev[1] - total_rev[0]) / total_rev[
            0
        ]  # This changes when the range of years the DCF uses changes
        ebit = [e - d_and_a for e, d_and_a in zip(ebitda, depreciationAndAmortization)]
        sharesOutstanding = marketCap / current_share_price
        effectiveTaxRate = (
            income_statement["incomeTaxExpense"] / income_statement["incomeBeforeTax"]
        )
        noplat = [e * (1 - effectiveTaxRate) for e in ebit]
        workingCapital = [
            tca - tcl
            for tca, tcl in zip(
                balance_sheet["totalCurrentAssets"],
                balance_sheet["totalCurrentLiabilities"],
            )
        ]
        average_rate_of_debt = (
            income_statement["interestExpense"] / balance_sheet["totalDebt"]
        ) * 1

        # DCF Valuation
        worksheet["C10"] = sharesOutstanding
        worksheet["C11"] = current_share_price

        # FCF Buildup
        letters = ["C", "D", "E"]
        for rev, letter in zip(total_rev[-3:], letters):
            worksheet[f"{letter}19"] = rev
        worksheet["C20"] = first_year_growth_rate
        for net_income, letter in zip(netIncome[-3:], letters):
            worksheet[f"{letter}21"] = net_income
        for noplat, letter in zip(noplat[-3:], letters):
            worksheet[f"{letter}24"] = noplat
        for dep_and_amort, letter in zip(depreciationAndAmortization[-3:], letters):
            worksheet[f"{letter}26"] = dep_and_amort
        for wc, letter in zip(workingCapital[-3:], letters):
            worksheet[f"{letter}28"] = wc
        for cap_expend, letter in zip(capitalExpenditure[-3:], letters):
            worksheet[f"{letter}30"] = cap_expend

        # WACC Calculation
        worksheet["C36"] = average_rate_of_debt
        worksheet["C37"] = effectiveTaxRate
        worksheet["C40"] = beta
        worksheet["E36"] = totalDebt
        worksheet["E37"] = marketCap

    workbook.save(dcf_analysis_path)


def comparables_analysis(
    filename: str,
    template_name: str = "Template",
    comparables_analysis_name: str = "comparables_analysis.xlsx",
) -> None:
    """
    Writes data from sqlite3 database to comparables_analysis.xlsx
    """
    companies = get_company_tickers(filename)
    comparables_analysis_path = os.path.join(
        resource_dirname, comparables_analysis_name
    )
    workbook = openpyxl.load_workbook(comparables_analysis_path)
    workbook.copy_worksheet(workbook[template_name])

    worksheet = workbook["Template Copy"]
    worksheet.title = " ".join(companies)

    starting_row = 7

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
            worksheet.insert_rows(starting_row)

    workbook.save(comparables_analysis_path)


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


def load_from_json(company: str, statement_type: str) -> list[dict[str, int | str]]:
    """
    Loads data from local json file and returns a dictionary
    """
    filepath = os.path.join(data_dirname, f"{statement_type}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return data[company]


def fetch_from_api(company: str, statement_type: str) -> list[dict[str, int | str]]:
    """
    Fetches data from the API and returns a dictionary
    """
    # NOTE Limit is set to 4 because we only want the last 4 years of data
    url = f"https://financialmodelingprep.com/api/v3/{statement_type}/{company}?apikey={API_KEY}&limit=4"
    response = requests.get(url)
    return response.json()


def save_to_db(
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


def _dcf_helper(
    company: str,
    db_path: str = "financial_data.db",
):

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    profile = {
        "price": 0.0,
        "mktCap": 0,
        "beta": 0.0,
    }
    income_statement = {
        "netIncome": [],
        "revenue": [],
        "ebitda": [],
        "depreciationAndAmortization": [],
        "incomeTaxExpense": 0,
        "incomeBeforeTax": 0,
        "interestExpense": 0,
    }
    balance_sheet = {
        "cashAndCashEquivalents": [],
        "totalCurrentAssets": [],
        "totalCurrentLiabilities": [],
        "totalDebt": 0,
    }
    cash_flow_statement = {
        "capitalExpenditure": [],
    }

    for value_type in profile:
        cursor.execute(f"SELECT {value_type} FROM profile WHERE symbol = '{company}'")
        profile[value_type] = cursor.fetchone()[0]

    for value_type in income_statement:
        cursor.execute(
            f"SELECT {value_type} FROM income_statement WHERE symbol = '{company}'"
        )
        if value_type in ["incomeTaxExpense", "incomeBeforeTax", "interestExpense"]:
            income_statement[value_type] = cursor.fetchone()[0]
        else:
            income_statement[value_type] = [tup[0] for tup in cursor.fetchall()]
    for value_type in balance_sheet:
        cursor.execute(
            f"SELECT {value_type} FROM balance_sheet WHERE symbol = '{company}'"
        )
        if value_type in ["totalDebt"]:
            balance_sheet[value_type] = cursor.fetchone()[0]
        else:
            balance_sheet[value_type] = [tup[0] for tup in cursor.fetchall()]
    for value_type in cash_flow_statement:
        cursor.execute(
            f"SELECT {value_type} FROM cash_flow_statement WHERE symbol = '{company}'"
        )
        cash_flow_statement[value_type] = [tup[0] for tup in cursor.fetchall()]

    return (
        profile,
        income_statement,
        balance_sheet,
        cash_flow_statement,
    )


def main():
    # companies = get_company_tickers("load.txt")
    # get_financials(companies)
    # comparables_analysis(companies)
    # dcf_analysis()
    pass


if __name__ == "__main__":
    main()
