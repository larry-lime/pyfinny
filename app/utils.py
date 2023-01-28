import subprocess
import os
import sqlite3
import platform


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
