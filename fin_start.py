from fin_analysis import *
from fin_compare import *
from fin_utils import *

def menu():
    print("\nType the number corresponding to the desired action:")
    # Menu display 1
    menu1 = input("\n1. Load companies\n2. Compare companies\n3. Exit Program\n> ")

    # Option 1
    if menu1 == "1":
        print(
            "\nYou have the following companies in your current folder:",
            list_companies(),
        )
        lst = []
        print("\nType the number corresponding to the desired action:")

        # Menu Display 1 of Option 1
        menu2 = input(
            "\n1. Manually input company ticker symbols\n2. Read ticker symbols from tickers.csv\n3. Exit Program\n> "
        )
        if menu2 == "1":
            while True:
                # Show companies in pwd
                print(
                    "\nYou have the following companies in your current folder:",
                    list_companies(),
                )
                ticker = input(
                    "Enter the ticker of a company you wish to load: "
                ).upper()
                if ticker == "START":
                    break
                else:
                    lst.append(ticker)
                    print("\nCompanies ready to load:", lst)
                    print("Type 'start' to load new companies")
        elif menu2 == "2":
            lst = read_tickers()

        elif menu2 == "3":
            pass
        else:
            print("Ivalid Input!")
            menu()

        if menu2 == "1" or menu2 == "2":
            for ticker in lst:
                company = Company(ticker)
                try:
                    lst = [
                        x[0].split("/")[-1] + "/" for x in os.walk(company._parent_dir)
                    ]
                    if company._dir not in lst:
                        company.import_data("annual")
                    company.load_binary_data()
                    company.convert_statements()
                    company.convert_statistics()
                    company.wacc()
                    company.save_as_xslx()
                    company.save_as_csv()
                except Exception as e:
                    error_log(e, company._parent_dir)
                    pass
            menu()

    # Option 2
    elif menu1 == "2":
        # Show companies in pwd
        lst = list_companies()
        companies = []
        print("\nThese are currently the companies you can compare:", lst, "\n")
        ticker = input(
            "Enter the ticker of the companys you wish to compare\nType 'start' to compare company statistics\nType 'all' to compare all companies\nType 'stop' to stop comparing\n> "
        ).upper()
        while True:
            if ticker == "START" or ticker == "STOP":
                break
            if ticker == "ALL":
                companies = lst
                break
            else:
                companies.append(ticker)
                print("\nThese are currently the companies you can compare:", lst)
                print("Current companies to be compared:", companies)
                ticker = input(
                    "\nEnter the ticker of the companys you wish to compare\nType 'start' when all companies are entered\nType 'stop' to stop comparing\n> "
                ).upper()
        if ticker != "STOP":
            compare = Compare(companies)
            compare.combine()
            compare.clean()
            compare.save_as_xslx()
            compare.save_as_csv()
            compare.save_as_txt()
            print("Done comparing companies!")
        menu()

    # Option 3
    elif menu1 == "3":
        print("Program Exited!")

    # Invalid Input
    else:
        print("Invalid input!")
        menu()

if __name__ == "__main__":
    print("\nWelcome to the Company Financials Analyzer!", end="")
    menu()
