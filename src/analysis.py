from utils import *
from yahoofinancials import YahooFinancials
import pandas as pd
import pickle as pk
import os


# TODO think about implementing threading to change the way this operates
class Company:
    def __init__(self, ticker: str):

        # Set the ticker
        self.ticker = ticker

        # Store financial statements and key statistics in a DataFrame
        self.fin_df = pd.DataFrame()
        self.stats = pd.DataFrame()

        # Store models as attributes
        self._wacc = pd.DataFrame()
        self._DCF = pd.DataFrame()

        # Path to files and directories
        self._parent_dir = os.getcwd()
        self._folder = "financials/"
        self._dir = f"{ticker}/"
        self._path = os.path.join(self._parent_dir, self._folder, self._dir)
        print("self._path:", self._path)
        print(
            "something else:", os.path.join(
                self._parent_dir, "financials", self.ticker)
        )

        # Create the folder if it doesn't exist
        if not os.path.isdir(self._folder):
            os.mkdir(self._folder)

    def import_data(self, a_or_q: str):
        """
        Import company financial statements and key statistics
        """
        # Create a company directory and initiate YahooFinancials
        None if os.path.isdir(self._path) else os.mkdir(self._path)
        yf = YahooFinancials(self.ticker)

        # Import data with the API
        fin_dic = yf.get_financial_stmts(a_or_q, ["balance", "income", "cash"])
        stats_dic = {
            "stats": yf.get_key_statistics_data(),
            "price": yf.get_current_price(),
            "mkt_cap": yf.get_market_cap(),
            "pe_ratio": yf.get_pe_ratio(),
            "div_yield": yf.get_dividend_yield(),
        }

        # Convert financial statements and key statistics to dataframes
        self.fin_df = self.__convert_fin(fin_dic)
        self.stats = self.__convert_stats(stats_dic)

    # TODO Refactor this if I can or delete it when I use a different API
    def __convert_fin(self, fin_dic):
        """
        Convert financial statements from dictionary to dataframe
        """
        for counter, i in enumerate(fin_dic, start=1):
            csv_df = pd.DataFrame()
            for j in fin_dic[i].keys():
                for k in fin_dic[i][j]:
                    for d in k.keys():
                        csv_series = pd.DataFrame(
                            list(k[d].values()),
                            index=list(k[d].keys()),
                            columns=[f"{j} {d}"],
                        )
                        csv_df = pd.concat([csv_df, csv_series], axis=1)

            if counter == 1:
                self._bl = csv_df
            elif counter == 2:
                self._inc = csv_df
            elif counter == 3:
                self._cf = csv_df

        # Concatenate the bl, inc, and cf dataframes
        return pd.concat([self._bl, self._inc, self._cf], axis=0)

    def __convert_stats(self, stats_dic):
        """
        Convert key statistics data from dictionary to dataframe
        """
        extra_stats = self.__calculate_additional_stats(stats_dic)
        og_stats = pd.DataFrame.from_dict(
            stats_dic["stats"][self.ticker], orient="index", columns=[self.ticker]
        )
        return pd.concat([extra_stats, og_stats], axis=0)

    def binary_files(self, save: bool = False, load: bool = False):
        """
        Save or load company financial and key statistics binaries
        """
        fin_name = f"{self.ticker}_financials_binary"
        stats_name = f"{self.ticker}_stats_binary"

        if save:
            with open(self._path + fin_name, "wb") as fin:
                pk.dump(self.fin_df, fin)
            with open(self._path + stats_name, "wb") as stats:
                pk.dump(self.stats, stats)

        if load:
            with open(self._path + fin_name, "rb") as fin:
                self.fin_df = pk.load(fin)
            with open(self._path + stats_name, "rb") as stats:
                self.stats = pk.load(stats)

    def __calculate_additional_stats(self, stats_dic):
        # TODO Refactor the following expressions for readability
        # Debt to Equity Ratio
        totalAssets = self.fin_df.loc["totalAssets", list(self.fin_df)[0]]
        totalLiabilities = self.fin_df.loc["totalLiab", list(self.fin_df)[0]]
        totalStockholderEquity = totalAssets - totalLiabilities
        debtToEquity = totalLiabilities / totalStockholderEquity

        # Outstanding Shares
        outstandingShares = stats_dic["mkt_cap"]/stats_dic["price"]

        # Return on equity (ROE)
        netIncome = list(self.fin_df.loc["netIncome", list(self.fin_df)[0]])[0]
        returnOnEquity = netIncome / totalStockholderEquity

        # Gross Profit Margin
        grossProfit = self.fin_df.loc["grossProfit", list(self.fin_df)[0]]
        totalRevenue = self.fin_df.loc["totalRevenue", list(self.fin_df)[0]]
        gp_margin = grossProfit / totalRevenue

        # Net Profit Margin
        netIncome = list(self.fin_df.loc["netIncome", list(self.fin_df)[0]])[0]
        np_margin = netIncome / totalRevenue

        # EBIT
        ebit = self.fin_df.loc["ebit", list(self.fin_df)[0]]

        return pd.DataFrame(
            [
                stats_dic["price"],
                stats_dic["pe_ratio"],
                stats_dic["mkt_cap"],
                outstandingShares,
                stats_dic["div_yield"],
                debtToEquity,
                returnOnEquity,
                gp_margin,
                np_margin,
                ebit,
            ],
            index=[
                "currentPrice",
                "peRatio",
                "marketCap",
                "outstandingShares",
                "divYield",
                "debtToEquity",
                "returnOnEquity",
                "grossProfitMargin",
                "netProfitMargin",
                "ebit",
            ],
            columns=[self.ticker],
        )

    # TODO Move this to another file
    def wacc(self):
        risk_free_rate = 0.02828
        market_rate_return = 0.105
        tax_rate = 0.21

        os.chdir(self._folder + self._dir)

        beta = float(self.stats[self.ticker]["beta"])
        market_risk_premium = market_rate_return - risk_free_rate
        # format the market risk premium to 2 decimal places
        debt = float(self.fin_df[list(self.fin_df)[0]]["longTermDebt"])
        equity = float(self.stats[self.ticker]["marketCap"])
        ebit = float(self.fin_df[list(self.fin_df)[0]]["ebit"])
        interestExpense = float(
            self.fin_df[list(self.fin_df)[0]]["interestExpense"])
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
        cost_of_debt = risk_free_rate + credit_spread
        cost_of_debt_after_tax = cost_of_debt * (1 - tax_rate)
        cost_of_equity = risk_free_rate + beta * market_risk_premium

        wacc = (equity / V) * cost_of_equity + \
            (debt / V) * cost_of_debt_after_tax
        self._wacc = pd.DataFrame(
            [
                wacc,
                beta,
                cost_of_debt,
                tax_rate,
                cost_of_debt_after_tax,
                risk_free_rate,
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
            self.fin_df.values,
            columns=self.fin_df.columns,
            index=[camel_to_normal(i) for i in self.fin_df.index],
        )

        # Save key statistics as xlsx file
        stats_df = pd.DataFrame(
            self.stats.values,
            columns=self.stats.columns,
            index=[camel_to_normal(i) for i in self.stats.index],
        )

        wacc_df = pd.DataFrame(
            self._wacc.values,
            columns=self._wacc.columns,
            index=[camel_to_normal(i) for i in self._wacc.index],
        )

        # Give the excel workbook a name
        xlsx_name = f"{self.ticker}_fin.xlsx"

        # Create the workbook
        # TODO Figureo out why I'm getting an error here
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
        self.fin_df.to_csv(self._path + csv_fin_name, index=True)
        self.stats.to_csv(self._path + csv_stats_name, index=True)
        self._wacc.to_csv(self._path + csv_wacc_name, index=True)

        # Print a confirmation message
        print(
            f"\
            \nFile: {csv_fin_name} created in {self._path}\
            \nFile: {csv_stats_name} created in {self._path}\
            \nFile: {csv_wacc_name} created in {self._path}"
        )

    # Convert financial statements and key statsitics to text files
    def save_as_txt(self):

        # Print a start message
        print("\nSaving financial and statistics data as TXT...")

        # Convert fin and stats from pandas DataFrame to string
        fin_str = self.fin_df.to_string()
        stats_str = self.stats.to_string()
        wacc_str = self._wacc.to_string()

        # Write fin, stats, and wacc to text file
        with open(self._path + f"{self.ticker}_fin.txt", "w") as file:
            file.write(fin_str)
        with open(self._path + f"{self.ticker}_stats.txt", "w") as file:
            file.write(stats_str)
        with open(self._path + f"{self.ticker}_wacc.txt", "w") as file:
            file.write(wacc_str)

        # Print a confirmation message
        print(
            f"\
            \nFile: {self.ticker}_fin.txt created in {self._path}\
            \nFile: {self.ticker}_stats.txt created in {self._path}\
            \nFile: {self.ticker}_wacc.txt created in {self._path}"
        )


if __name__ == "__main__":
    company = Company("DOX")
    company.import_data("annual")
    company.binary_files(save=True)
    company.binary_files(load=True)
    company.wacc()
    company.save_as_xslx()
    company.save_as_csv()
    company.save_as_txt()
