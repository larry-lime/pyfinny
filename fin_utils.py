import pandas as pd
import os


def list_companies():
    parent_dir = "financials"
    return [i for i in list(os.listdir(f"./{parent_dir}")) if os.path.isdir(f"{parent_dir}/{i}")] if parent_dir in os.listdir(".") else []

# Create an error log binary file in the current directory
def error_log(e, parent_dir):
    # Change working directory to parent directory
    os.chdir(parent_dir)
    with open("error_log.txt", "a") as f:
        f.write(str(e) + "\n")


# Write a function that reads tickers.csv
def read_tickers():
    # Change pwd to parent directory
    os.chdir(os.getcwd())

    # Read tickers.csv
    tickers_df = pd.read_csv("tickers.csv")

    # Return tickers_df
    column = list(tickers_df.columns)[0]

    return [i.strip() for i in tickers_df[column]]


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
