from fin_utils import *
from yahoofinancials import YahooFinancials 
import pandas as pd
import pickle as pk
import os

class Company:
    def __init__(self, ticker: str) -> None:

        # Set the ticker
        self.ticker = ticker

        # Store Statements as attributes
        self._bl = pd.DataFrame()
        self._cf = pd.DataFrame()
        self._inc = pd.DataFrame()
        self._fin = pd.DataFrame()
        self._wacc = pd.DataFrame()

        # Store stats as attributes
        self._stats = pd.DataFrame()
        self._pe = pd.DataFrame()
        self._mkt_cap = pd.DataFrame()
        self._div_yield = pd.DataFrame()
        self._parent_dir = os.getcwd()
        self._folder = "company_financials/"

        if not os.path.isdir(self._folder):
            os.mkdir(self._folder)
        # Change working directory to the company_financials folder
        self._dir = f"{ticker}_fin/"
        # Store File Directory Information
        self._path = os.path.join(self._parent_dir, self._folder, self._dir)

    # Import and save Yahoo Financials data as binary files
    def import_data(self, annual_or_quarterly: str):

        if not os.path.isdir(self._path):
            os.mkdir(self._path)

        # Print a start mesage
        print()
        print(f"Fetching ({self.ticker}) Data from Yahoo Finance (This may take a while so grab a snack or something)...")

        # Create the YahooFinancials object
        yf = YahooFinancials(self.ticker)

        print(f"Importing ({self.ticker}) Financial Data...")
        # Get the financial statements
        self._fin = yf.get_financial_stmts(
            annual_or_quarterly, ["balance", "income", "cash"]
        )
        print("Financial statements done importing!")

        print(f"Importing ({self.ticker}) Statistics Data...")
        # Get the key statistics
        stats = {
            "stats": yf.get_key_statistics_data(),
            "mkt_cap": yf.get_market_cap(),
            "pe_ratio": yf.get_pe_ratio(),
            "div_yield": yf.get_dividend_yield(),
        }
        print("Key statistics done importing!")

        # Give the binary files names
        financials_file_name = f"{self.ticker}_financials_binary"
        stats_file_name = f"{self.ticker}_stats_binary"

        # Save the financial statements as binary files
        with open(self._path + financials_file_name, "wb") as file_object:
            pk.dump(self._fin, file_object)
        with open(self._path + stats_file_name, "wb") as file_object:
            pk.dump(stats, file_object)

        # Print a confirmation message
        print()
        print(f"File: {financials_file_name} created in {self._path}")
        print(f"File: {stats_file_name} created in {self._path}")

    # Load company financial and statistics data from binary files
    def load_binary_data(self):

        # Print a start mesage
        print(f"\nLoading ({self.ticker}) Data...")

        # Assign which binary files to load
        financials_file_name = f"{self.ticker}_financials_binary"
        stats_file_name = f"{self.ticker}_stats_binary"

        # Load the financial statements as dictionaries
        with open(self._path + financials_file_name, "rb") as fin:
            self._fin = pk.load(fin)
        with open(self._path + stats_file_name, "rb") as stats:
            stats = pk.load(stats)

        # Unpack the dictionaries
        self._stats = stats["stats"]
        self._mkt_cap = stats["mkt_cap"]
        self._pe = stats["pe_ratio"]
        self._div_yield = stats["div_yield"]

        # Print a confirmation message
        print("Data done loading!")

    # Convert self._fin from a dictionary to a pandas DataFrame
    def convert_statements(self):

        # Print a start mesage
        print("\nConverting financial statements...")

        # Iterate through the nested dictionary and assign values to new DataFrame
        fin = self._fin
        counter = 0
        for i in fin:
            counter += 1
            csv_df = pd.DataFrame()
            for j in fin[i].keys():
                for k in fin[i][j]:
                    for d in k.keys():
                        csv_series = pd.DataFrame(
                            [i for i in k[d].values()],
                            index=[i for i in k[d].keys()],
                            columns=[f"{j} {d}"],
                        )
                        csv_df = pd.concat([csv_df, csv_series], axis=1)

            # Assign the DataFrames to attribute
            if counter == 1:
                self._bl = csv_df
            elif counter == 2:
                self._inc = csv_df
            elif counter == 3:
                self._cf = csv_df

        # Concatenate the bl, inc, and cf DataFrames into one
        self._fin = pd.concat([self._bl, self._inc, self._cf], axis=0)

        # Drop duplicates from the dataframe
        # self._fin = self._fin.drop_duplicates(subset=list(self._fin)[0],inplace=False,keep='first')

        # Print a confirmation message
        print("Financial statements done converting!")

    # Convert self._stats from a dictionary to a pandas DataFrame
    def convert_statistics(self):

        # Print a start mesage
        print("\nConverting key statistics...")

        # DE Ratio
        # totalStockholderEquity = self._fin['totalStockholderEquity'][list(self._fin)[0]]
        totalAssets = self._fin.loc["totalAssets", list(self._fin)[0]]
        totalLiabilities = self._fin.loc["totalLiab", list(self._fin)[0]]
        totalStockholderEquity = totalAssets - totalLiabilities
        debtToEquity = (
            totalLiabilities / totalStockholderEquity
        )  # This can use some work

        # ROE
        netIncome = list(self._fin.loc["netIncome", list(self._fin)[0]])[0]
        returnOnEquity = netIncome / totalStockholderEquity

        # GP Margin
        # grossProfit = list(self._fin.loc["grossProfit", list(self._fin)[0]])[0]
        grossProfit = self._fin.loc["grossProfit", list(self._fin)[0]]
        # totalRevenue = list(self._fin.loc["totalRevenue", list(self._fin)[0]])[0]
        totalRevenue = self._fin.loc["totalRevenue", list(self._fin)[0]]
        GP_margin = grossProfit / totalRevenue

        # NP Margin
        netIncome = list(self._fin.loc["netIncome", list(self._fin)[0]])[0]
        NP_margin = netIncome / totalRevenue

        # EBIT
        ebit = self._fin.loc["ebit", list(self._fin)[0]]

        # Price To Sales
        # ps = self._mkt_cap / totalRevenue

        # Create a dataframe with integers self._pe and self._mkt_cap
        temp = pd.DataFrame(
            [
                self._pe,
                self._mkt_cap,
                self._div_yield,
                debtToEquity,
                returnOnEquity,
                GP_margin,
                NP_margin,
                ebit,
            ],
            index=[
                "peRatio",
                "marketCap",
                "divYield",
                "debtToEquity",
                "returnOnEquity",
                "grossProfitMargin",
                "netProfitMargin",
                "ebit",
            ],
            columns=[self.ticker],
        )

        # Convert dictionary to DataFrame
        self._stats = pd.DataFrame.from_dict(
            self._stats[self.ticker], orient="index", columns=[self.ticker]
        )

        # Append the temp DataFrame to the self._stats DataFrame
        self._stats = pd.concat([temp, self._stats], axis=0)

        # Print a confirmation message
        print("Key statistics done converting!")

    def wacc(self):
        self.risk_free_rate = 0.02828
        self.market_rate_return = 0.105
        self.tax_rate = 0.21

        ticker = self.ticker
        self._dir = f"{ticker}_fin/"
        os.chdir(self._folder + self._dir)

        stats_df = self._stats
        beta = float(stats_df[ticker]["beta"])
        market_risk_premium = self.market_rate_return - self.risk_free_rate
        # format the market risk premium to 2 decimal places
        fin_df = self._fin
        debt = float(fin_df[list(fin_df)[0]]["longTermDebt"])
        equity = float(stats_df[ticker]["marketCap"])
        ebit = float(fin_df[list(fin_df)[0]]["ebit"])
        interestExpense = float(fin_df[list(fin_df)[0]]["interestExpense"])
        interest_coverage_ratio = ebit / interestExpense
        credit_spread = 0

        if interest_coverage_ratio > -100000 and interest_coverage_ratio <= 0.499999:
            credit_spread = 14.34 / 100
        if interest_coverage_ratio > 0.5 and interest_coverage_ratio <= 0.799999:
            credit_spread = 10.76 / 100
        if interest_coverage_ratio > 0.8 and interest_coverage_ratio <= 1.249999:
            credit_spread = 8.80 / 100
        if interest_coverage_ratio > 1.25 and interest_coverage_ratio <= 1.499999:
            credit_spread = 7.78 / 100
        if interest_coverage_ratio > 1.5 and interest_coverage_ratio <= 1.999999:
            credit_spread = 4.62 / 100
        if interest_coverage_ratio > 2 and interest_coverage_ratio <= 2.499999:
            credit_spread = 3.78 / 100
        if interest_coverage_ratio > 2.5 and interest_coverage_ratio <= 2.999999:
            credit_spread = 3.15 / 100
        if interest_coverage_ratio > 3 and interest_coverage_ratio <= 3.499999:
            credit_spread = 2.15 / 100
        if interest_coverage_ratio > 3.5 and interest_coverage_ratio <= 3.9999999:
            credit_spread = 1.93 / 100
        if interest_coverage_ratio > 4 and interest_coverage_ratio <= 4.499999:
            credit_spread = 1.59 / 100
        if interest_coverage_ratio > 4.5 and interest_coverage_ratio <= 5.999999:
            credit_spread = 1.29 / 100
        if interest_coverage_ratio > 6 and interest_coverage_ratio <= 7.499999:
            credit_spread = 1.14 / 100
        if interest_coverage_ratio > 7.5 and interest_coverage_ratio <= 9.499999:
            credit_spread = 1.03 / 100
        if interest_coverage_ratio > 9.5 and interest_coverage_ratio <= 12.499999:
            credit_spread = 0.82 / 100
        if interest_coverage_ratio > 12.5 and interest_coverage_ratio <= 100000:
            credit_spread = 0.67 / 100

        V = equity + debt
        cost_of_debt = self.risk_free_rate + credit_spread
        cost_of_debt_after_tax = cost_of_debt * (1 - self.tax_rate)
        cost_of_equity = self.risk_free_rate + beta * market_risk_premium

        wacc = (equity / V) * cost_of_equity + (debt / V) * cost_of_debt_after_tax
        self._wacc = pd.DataFrame(
            [
                wacc,
                beta,
                cost_of_debt,
                self.tax_rate,
                cost_of_debt_after_tax,
                self.risk_free_rate,
                cost_of_equity,
                debt,
                equity,
                ebit,
                interest_coverage_ratio,
                interestExpense,
                credit_spread,
            ],
            index=[
                "wacc",
                "beta",
                "costOfDebt",
                "taxRate",
                "costOfDebtAfterTax",
                "riskFreeRate",
                "costOfEquity",
                "debt",
                "equity",
                "ebit",
                "interestCoverageRatio",
                "interestExpense",
                "creditSpread",
            ],
            columns=[self.ticker],
        )

        os.chdir(self._parent_dir)

    # Save bl, inc, cf, fin, and stats as xlsx files in company directory
    def save_as_xslx(self):

        # Print a start message
        print("\nSaving financial and statistics data as Excel...")

        # Save the financial statements as xlsx files
        bl_df = pd.DataFrame(
            self._bl.values,
            columns=self._bl.columns,
            index=[camel_to_normal(i) for i in self._bl.index],
        )
        cf_df = pd.DataFrame(
            self._cf.values,
            columns=self._cf.columns,
            index=[camel_to_normal(i) for i in self._cf.index],
        )
        inc_df = pd.DataFrame(
            self._inc.values,
            columns=self._inc.columns,
            index=[camel_to_normal(i) for i in self._inc.index],
            # Save concatenated financial statements as xlsx files
        )
        fin_df = pd.DataFrame(
            self._fin.values,
            columns=self._fin.columns,
            index=[camel_to_normal(i) for i in self._fin.index],
        )

        # Save key statistics as xlsx file
        stats_df = pd.DataFrame(
            self._stats.values,
            columns=self._stats.columns,
            index=[camel_to_normal(i) for i in self._stats.index],
        )

        wacc_df = pd.DataFrame(
            self._wacc.values,
            columns=self._wacc.columns,
            index=[camel_to_normal(i) for i in self._wacc.index],
        )

        # Give the excel workbook a name
        xlsx_name = f"{self.ticker}_fin.xlsx"

        # Create the workbook
        with pd.ExcelWriter(self._path + xlsx_name) as writer:

            # Save the dataframes as workbook sheets
            bl_df.to_excel(writer, sheet_name="Balance Sheet")
            inc_df.to_excel(writer, sheet_name="Income Statement")
            cf_df.to_excel(writer, sheet_name="Cash Flow")
            fin_df.to_excel(writer, sheet_name="Financials")
            stats_df.to_excel(writer, sheet_name="Key Statistics")
            wacc_df.to_excel(writer, sheet_name="WACC")

        # Print a confirmation message
        print(f"File: {xlsx_name} created in {self._path}")

    # Save fin as a csv file in company directory
    def save_as_csv(self):

        # Print a start message
        print("\nSaving financial and statistics data as CSV...")

        # Give the csv file a name
        csv_fin_name = f"{self.ticker}_fin.csv"
        csv_stats_name = f"{self.ticker}_stats.csv"
        csv_wacc_name = f"{self.ticker}_wacc.csv"

        # Save concatenated financial statements as csv files
        self._fin.to_csv(self._path + csv_fin_name, index=True)
        self._stats.to_csv(self._path + csv_stats_name, index=True)
        self._wacc.to_csv(self._path + csv_wacc_name, index=True)

        # Print a confirmation message
        print(f"File: {csv_fin_name} created in {self._path}")
        print(f"File: {csv_stats_name} created in {self._path}")
        print(f"File: {csv_wacc_name} created in {self._path}")

    # Convert financial statements and key statsitics to text files
    def save_as_txt(self):

        # Print a start message
        print("\nWriting data...")

        # Convert fin and stats from pandas DataFrame to string
        stats_str = self._fin.to_string()
        stats_str = self._stats.to_string()

        # Write fina fin and stats to text file
        with open(self._path + f"{self.ticker}_fin.txt", "w") as file:
            file.write(stats_str)
            print(f"{self.ticker}_fin.txt created in {self._path}")
        with open(self._path + f"{self.ticker}_stats.txt", "w") as file:
            print(f"{self.ticker}_stats.txt created in {self._path}")
            file.write(stats_str)

        # Print a confirmation message
        print("Data done writing!")


class Compare:
    def __init__(self, companies=[]):
        self.companies = companies
        self.stats_compare = pd.DataFrame()
        self.wacc_compare = pd.DataFrame()
        self._parent_dir = os.getcwd()
        self._folder = "company_financials/"

    # It needs to search in the current directory and find the csv files -> load the csv files -> combine them
    def combine(self):
        for ticker in self.companies:
            self._dir = f"{ticker}_fin/"
            os.chdir(self._folder + self._dir)

            # Read the stats csv files
            try:
                # Read the stats csv files
                stats_df = pd.read_csv(f"{ticker}_stats.csv", index_col=0)
                # Rename all the index to normal
                stats_df.index = [camel_to_normal(i) for i in stats_df.index]
                # Concatenate the stats_df to the stats_compare
                self.stats_compare = pd.concat([self.stats_compare, stats_df], axis=1)

            except Exception as error:
                error_log(error, self._parent_dir)
                pass

            try:
                # Read the wacc csv file
                wacc_df = pd.read_csv(f"{ticker}_wacc.csv", index_col=0)
                # Rename all the index to normal
                wacc_df.index = [camel_to_normal(i) for i in wacc_df.index]
                # Concatenate the wacc_df to the wacc_compare
                self.wacc_compare = pd.concat([self.wacc_compare, wacc_df], axis=1)

            except Exception as error:
                error_log(error, self._parent_dir)
                pass

            os.chdir(self._parent_dir)

    def clean(self):
        # Convert values in datafame from string to float
        # Swap axes of self.stats_compare
        self.stats_compare = self.stats_compare.T
        # Swap axes of self.wacc_compare
        self.wacc_compare = self.wacc_compare.T
        for i in self.stats_compare.columns:
            for j in self.stats_compare.index:
                try:
                    self.stats_compare[i][j] = float(self.stats_compare[i][j])
                except:
                    continue

    def save_as_xslx(self):
        # Save the stats_compare as xlsx file
        xlsx_name = "compare.xlsx"
        os.chdir(self._parent_dir)
        with pd.ExcelWriter(xlsx_name) as writer:
            # Save the dataframes as workbook sheets
            self.stats_compare.to_excel(writer, sheet_name="Comparables")
            self.wacc_compare.to_excel(writer, sheet_name="WACC Comparables")
        print(f"\nFile: {xlsx_name} created in {self._parent_dir}")

    def save_as_csv(self):
        # Save the stats_compare as csv file
        stats_csv_name = "stats_compare.csv"
        # Save the wacc compare as csv file
        wacc_csv_name = "wacc_compare.csv"
        os.chdir(self._parent_dir)
        self.stats_compare.to_csv(stats_csv_name)
        self.wacc_compare.to_csv(wacc_csv_name)

        print(f"File: {stats_csv_name} created in {self._parent_dir}")
        print(f"File: {wacc_csv_name} created in {self._parent_dir}")

    def save_as_txt(self):

        # Print a start message
        print("\nWriting data...")

        # Convert fin and stats from pandas DataFrame to string
        stats_txt_name = "stats_compare.txt"
        wacc_txt_name = "wacc_compare.txt"
        os.chdir(self._parent_dir)
        stats_str = self.stats_compare.to_string()
        wacc_str = self.wacc_compare.to_string()
        # Write fina fin and stats to text file
        with open(stats_txt_name, "w") as file:
            file.write(stats_str)
        with open(wacc_txt_name, "w") as file:
            file.write(wacc_str)
        print(f"File: {stats_txt_name} created in {self._parent_dir}")
        print(f"File: {wacc_txt_name} created in {self._parent_dir}")


if __name__ == "__main__":
    # company = Company("DOX")
    # company.import_data("quarterly")
    # company.load_binary_data()
    # company.convert_statements()
    # company.convert_statistics()
    # company.wacc()
    # company.save_as_xslx()
    # company.save_as_csv()
    # compare = Compare(['TSLA', 'TSEM'])
    # compare.combine()
    # compare.clean()
    # compare.save_as_xslx()
    # compare.save_as_txt()
    # compare.save_as_csv()
    pass
