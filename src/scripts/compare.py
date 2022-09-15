import itertools
from utils import *
import pandas as pd
import os


class Compare:
    def __init__(self, companies=None):
        if companies is None:
            companies = []
        self.companies = companies
        self.stats_compare = pd.DataFrame()
        self.wacc_compare = pd.DataFrame()
        self.parent_dir = os.getcwd()
        self.comparables_folder = f"{os.getcwd()}/comparables/"
        self.financials_folder = "financials/"

        # Create the folder if it doesn't exist
        if not os.path.isdir(self.comparables_folder):
            os.mkdir(self.comparables_folder)

    # It needs to search in the current directory and find the csv files -> load the csv files -> combine them
    def combine(self):
        for ticker in self.companies:
            self._dir = f"{ticker}/"
            os.chdir(self.financials_folder + self._dir)

            # Read the stats csv files
            try:
                # Read the stats csv files
                stats_df = pd.read_csv(f"{ticker}_stats.csv", index_col=0)
                # Rename all the index to normal
                stats_df.index = [camel_to_normal(i) for i in stats_df.index]
                # Concatenate the stats_df to the stats_compare
                self.stats_compare = pd.concat([self.stats_compare, stats_df], axis=1)

            except Exception as error:
                # TODO trigger the error log in the same way that analysis does
                error_log(error, self.parent_dir)

            try:
                # Read the wacc csv file
                wacc_df = pd.read_csv(f"{ticker}_wacc.csv", index_col=0)
                # Rename all the index to normal
                wacc_df.index = [camel_to_normal(i) for i in wacc_df.index]
                # Concatenate the wacc_df to the wacc_compare
                self.wacc_compare = pd.concat([self.wacc_compare, wacc_df], axis=1)

            except Exception as error:
                error_log(error, self.parent_dir)

            os.chdir(self.parent_dir)

    def clean(self):
        # Convert values in datafame from string to float
        # Swap axes of self.stats_compare
        self.stats_compare = self.stats_compare.T
        # Swap axes of self.wacc_compare
        self.wacc_compare = self.wacc_compare.T
        for i, j in itertools.product(
            self.stats_compare.columns, self.stats_compare.index
        ):
            try:
                self.stats_compare[i][j] = float(self.stats_compare[i][j])
            except Exception:
                continue

    def save_as_xslx(self):
        # Save the stats_compare as xlsx file
        xlsx_name = f"{self.comparables_folder}compare.xlsx"
        os.chdir(self.comparables_folder)
        with pd.ExcelWriter(xlsx_name) as writer:
            # Save the dataframes as workbook sheets
            self.stats_compare.to_excel(writer, sheet_name="Comparables")
            self.wacc_compare.to_excel(writer, sheet_name="WACC Comparables")
        print(f"\nFile: {xlsx_name} created in {self.comparables_folder}")

    def save_as_csv(self):
        # Save the stats_compare as csv file
        stats_csv_name = f"{self.comparables_folder}stats_compare.csv"
        # Save the wacc compare as csv file
        wacc_csv_name = f"{self.comparables_folder}wacc_compare.csv"
        os.chdir(self.parent_dir)
        self.stats_compare.to_csv(stats_csv_name)
        self.wacc_compare.to_csv(wacc_csv_name)

        print(f"File: {stats_csv_name} created in {self.comparables_folder}")
        print(f"File: {wacc_csv_name} created in {self.comparables_folder}")

    def save_as_txt(self):

        # Print a start message
        print("\nWriting data...")

        # Convert fin and stats from pandas DataFrame to string
        stats_txt_name = f"{self.comparables_folder}stats_compare.txt"
        wacc_txt_name = f"{self.comparables_folder}wacc_compare.txt"
        os.chdir(self.parent_dir)
        stats_str = self.stats_compare.to_string()
        wacc_str = self.wacc_compare.to_string()
        # Write fina fin and stats to text file
        with open(stats_txt_name, "w") as file:
            file.write(stats_str)
        with open(wacc_txt_name, "w") as file:
            file.write(wacc_str)
        print(f"File: {stats_txt_name} created in {self.comparables_folder}")
        print(f"File: {wacc_txt_name} created in {self.comparables_folder}")


if __name__ == "__main__":
    compare = Compare(["TSLA", "TSEM"])
    compare.combine()
    compare.clean()
    compare.save_as_xslx()
    compare.save_as_csv()
    compare.save_as_txt()
