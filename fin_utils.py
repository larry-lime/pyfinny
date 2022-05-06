import pandas as pd
import os
def list_companies():
    return [
        i.split("_")[0] for i in [x[0].split("/")[-1] for x in os.walk(os.getcwd())][2:]
    ]


# Create an error log binary file in the current directory
def error_log(e, parent_dir):
    # Change working directory to parent directory
    os.chdir(parent_dir)
    f = open("error_log.txt", "a")
    f.write(str(e) + "\n")
    f.close()


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
    lst = [i for i in camel]
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
