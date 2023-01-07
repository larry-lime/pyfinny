from analysis import *
from compare import *
from utils import *


# TODO As the project gets larger, break up this file into an analysis and compare CMD
class Start:
    def __init__(self) -> None:
        self.load_company_list = []
        self.compare_company_list = []

    def main_menu(self, message=None):
        # Menu Display
        if message == "inputInvalid":
            menu_input = input(
                "\
                \n┌─Main Menu───────────────────────────────────────────┐\
                \n│Type the number corresponding to the desired action: │\
                \n└─────────────────────────────────────────────────────┘\
                \n┌─Message─────────────────────────────────────────────┐\
                \n│Input Invalid!                                       │\
                \n└─────────────────────────────────────────────────────┘\
                \n1. Load companies\
                \n2. Compare companies\
                \n3. Exit Program\
                \n> "
            )
        else:
            menu_input = input(
                "\
                \n┌─Main Menu───────────────────────────────────────────┐\
                \n│Type the number corresponding to the desired action: │\
                \n└─────────────────────────────────────────────────────┘\
                \n1. Load companies\
                \n2. Compare companies\
                \n3. Exit Program\
                \n> "
            )

        # Read Menu Input
        if menu_input == "1":
            self.load_companies()
        elif menu_input == "2":
            self.compare_companies()
        elif menu_input == "3":
            self.exit_menu()
        else:
            self.invalid_input("inputInvalid", self.main_menu)

    # Submenu 1
    def load_companies(self, message=None):

        if message == "inputInvalid":
            submenu_input = input(
                "\
                \n┌─Load Companies──────────────────────────────────────┐\
                \n│Type the number corresponding to the desired action: │\
                \n└─────────────────────────────────────────────────────┘\
                \n┌─Message─────────────────────────────────────────────┐\
                \n│Input Invalid!                                       │\
                \n└─────────────────────────────────────────────────────┘\
                \n1. Manually input company ticker symbols\
                \n2. Read ticker symbols from tickers.csv\
                \n3. Go Back\
                \n4. Exit Program\
                \n> "
            )
        else:
            submenu_input = input(
                "\
                \n┌─Load Companies──────────────────────────────────────┐\
                \n│Type the number corresponding to the desired action: │\
                \n└─────────────────────────────────────────────────────┘\
                \n1. Manually input company ticker symbols\
                \n2. Read ticker symbols from tickers.csv\
                \n3. Go Back\
                \n4. Exit Program\
                \n> "
            )

        if submenu_input in ["1", "2"]:
            load_list = self.manual_input() if submenu_input == "1" else read_tickers()
            self.run_load(load_list)
            self.main_menu()
        elif submenu_input == "3":
            self.main_menu()
        elif submenu_input == "4":
            self.exit_menu()
        else:
            self.invalid_input("inputInvalid", self.load_companies)

    def manual_input(self):

        user_input = input(
            f"\
            \n┌─Manual Input────────────────────────────────────────┐\
            \n│Type the ticker of the company you wish to load:     │\
            \n│                                                     │\
            \n│                        OR                           │\
            \n│                                                     │\
            \n│Type the number corresponding to the desired action: │\
            \n└─────────────────────────────────────────────────────┘\
            \nCompanies ready to load: {self.load_company_list}\
            \n1. Start loading company data\
            \n2. Undo last entry\
            \n3. Clear company list\
            \n4. Go Back\
            \n5. Exit Program\
            \n> "
        )

        if user_input == "1":
            return self.load_company_list
        elif user_input == "2":
            self.load_company_list.pop()
        elif user_input == "3":
            self.load_company_list.clear()
        elif user_input == "4":
            self.load_companies()
        elif user_input == "5":
            self.exit_menu()

        else:
            self.load_company_list.append(
                user_input.upper()
            ) if user_input.upper() not in self.load_company_list else None

        return self.manual_input()

    def run_load(self, company_list):  # sourcery skip: class-extract-method
        for ticker in company_list:
            company = Company(ticker)
            try:
                loaded_companies = list_companies()
                # TODO Change the nine value so it counts how many files there are in a sample directory or not
                if (
                    company.ticker not in loaded_companies
                    or count_files(company_dir=company._dir) < 9
                ):
                    company.import_data("annual")
                company.binary_files(save=True)
                company.binary_files(load=True)
                company.wacc()
                company.save_as_xslx()
                company.save_as_csv()
                company.save_as_txt()

            except Exception as e:
                error_log(e, company._parent_dir)

    # Menu Input 2
    def compare_companies(self):
        company_list = list_companies()
        # TODO Fix the bug that occurs when I undo the last entry
        # Put this task on hold and instead work on the actual final product
        # Take into account how people want to compare companies
        # It's easiest for me to give people a directory name containing
        # Containing all the countries they want to compare
        # This will give me more room for improvement
        # How the folders get into that directory is not my problem
        submenu_input = input(
            f"\
            \n┌─Compare Companies───────────────────────────────────┐\
            \n│Type the ticker of the company you wish to compare:  │\
            \n│                                                     │\
            \n│                          OR                         │\
            \n│                                                     │\
            \n│Type the number corresponding to the desired action: │\
            \n└─────────────────────────────────────────────────────┘\
            \nAvailable Companies: {company_list}\
            \nCompare companies in: directory\
            \nCompanies ready to compare: {self.compare_company_list}\
            \n1. Start comparable analysis\
            \n2. Compare all available companies\
            \n3. Undo last entry\
            \n4. Go Back\
            \n5. Exit Program\
            \n> "
        )

        if submenu_input in ["1", "2"]:
            comparable_list = (
                self.compare_company_list if submenu_input == "1" else company_list
            )
            self.run_compare(comparable_list)
            self.main_menu()
        elif submenu_input == "3":
            # self.compare_company_list.pop() if self.compare_company_list else None
            self.compare_company_list.pop()
        elif submenu_input == "4":
            self.main_menu()
        elif submenu_input == "5":
            self.exit_menu()
        else:
            self.compare_company_list.append(
                submenu_input.upper()
            ) if submenu_input.upper() not in self.compare_company_list else None

        self.compare_companies()

    def run_compare(self, companies):
        compare = Compare(companies)
        compare.combine()
        compare.clean()
        compare.save_as_xslx()
        compare.save_as_csv()
        compare.save_as_txt()
        print("Done comparing companies!")

    def invalid_input(self, message=None, function=None):
        """
        Prints -> "Invalid Function" and calls the name of the function passed
        """
        if function and message:
            function(message)
        elif function:
            print("Invalid Input!")
            function()
        else:
            print("Invalid Input!")

    def exit_menu(self):
        print("Program Exited!")
        exit()


if __name__ == "__main__":
    print("\nWelcome to the Company Financials Analyzer!", end="")
    start = Start()
    start.main_menu()
