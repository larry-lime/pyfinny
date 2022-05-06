from fin_utils import *
import pandas as pd
import os

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
    compare = Compare(['TSLA', 'TSEM'])
    compare.combine()
    compare.clean()
    compare.save_as_xslx()
    compare.save_as_csv()
    compare.save_as_txt()
