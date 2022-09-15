from datetime import datetime
import pandas as pd
import os


def list_companies(parent_dir="financials"):
    return (
        [
            company
            for company in list(os.listdir(f"./{parent_dir}"))
            if os.path.isdir(f"{parent_dir}/{company}")
        ]
        if parent_dir in os.listdir(".")
        else []
    )


# TODO rename this and make this function check if the directory is full return a boolean
def count_files(company_dir,parent_dir="financials"):
    """
    Count the number of files in a given directory
    """
    return len(list(os.listdir(f"./{parent_dir}/{company_dir}")))


# Create an error log binary file in the current directory
def error_log(e, parent_dir):
    # Change working directory to parent directory

    # dd/mm/YY H:M:S
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    os.chdir(parent_dir)
    with open("error_log.txt", "a") as f:
        # f.write(str(e) + "\n")
        f.write(f"{str(e)} {dt_string}\n")


# Write a function that reads tickers.csv
def read_tickers(
    tickers_dir: str = "tickers",
    ticker_file: str = "sample_tickers",
    column_name=None,
) -> list[str]:

    # Read tickers.csv
    tickers_df = pd.read_csv(f"./{tickers_dir}/{ticker_file}.csv")

    # Return values in a column if a column is given, else the return the values in the first column
    if column_name:
        return [i.strip() for i in tickers_df[column_name]]
    return [i.strip() for i in tickers_df[list(tickers_df.columns)[0]]]


def camel_to_normal(camel: str):
    lst = list(camel)
    while True:
        cap = True
        for i in range(len(lst)):
            if lst[i].isupper() == True:
                lst[i] = " " + lst[i]
            else:
                cap = False
        if cap:
            return camel
        return "".join(lst).title()


def main():
    print(list_companies())


if __name__ == "__main__":
    main()
