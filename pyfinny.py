from app import application, utils
import click
import os


@click.group()
def cli():
    pass


@cli.command()
def setup():
    """
    Run the setup command before you begin analyzing
    """
    api_key = click.prompt("Enter your Financial Modelling Prep API Key")
    utils.set_api_key(api_key)
    utils.make_database()
    click.echo("Setup complete")


@cli.command()
@click.argument(
    "filename",
    type=str,
)
@click.option(
    "-d",
    "--resource_dir",
    type=str,
    help="Name of directory with Excel Files",
    default="resources",
)
def open(filename, resource_dir):
    """
    Open the excel file
    """
    utils.open_xlsx(resource_dir, f"{filename}.xlsx")


@cli.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    help="File with tickers to load",
    default="load.txt",
)
def load(filename):
    """
    Loads company financial statements
    """
    application.get_financials(filename)


@cli.command()
@click.option(
    "-t",
    "--table",
    type=str,
    help="Name of table to print",
)
def data(table):
    """
    Prints print data from database
    """
    # Ask the user if they want to print all tables
    boolean = click.prompt("Do you want to print all financial statement data (y/n)")
    if boolean == "y":
        for table in utils.get_tables():
            utils.show_data(table[0])
        return
    else:
        bal = click.prompt("Do you want to print the balance sheet? (y/n)")
        inc = click.prompt("Do you want to print the income statement? (y/n)")
        cash = click.prompt("Do you want to print the cash flow statement? (y/n)")
        prof = click.prompt("Do you want to print the company profile? (y/n)")
        if bal == "y":
            utils.show_data("balance_sheet")
        if inc == "y":
            utils.show_data("income_statement")
        if cash == "y":
            utils.show_data("cash_flow_statement")
        if prof == "y":
            utils.show_data("profile")


@cli.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    default="load.txt",
    help="File with tickers to use for DCF",
)
@click.option(
    "-d",
    "--ticker_dir",
    type=str,
    help="Name of directory with ticker files",
    # Directory containing venv
    default="tickers",
)
def tickers(filename, ticker_dir):
    """
    Prints tickers in file
    """
    for filename in os.listdir(ticker_dir):
        click.echo(filename)
        click.echo("---------------")
        [click.echo(i) for i in application.get_company_tickers(filename)]
        click.echo("---------------")


@cli.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    default="dcf.txt",
    help="File with tickers to use for DCF",
)
@click.option(
    "-t",
    "--template_name",
    type=str,
    help="Name of excel sheet with DCF template",
    default="Template",
)
@click.option(
    "-n",
    "--dcf_analysis_name",
    type=str,
    help="Name of excel file with DCF template",
    default="dcf.xlsx",
)
def dcf(filename, template_name, dcf_analysis_name):
    """
    Discounted Cash Flow
    """
    application.dcf_analysis(filename, template_name, dcf_analysis_name)
    click.echo(f"Wrote to {dcf_analysis_name}")


@cli.command()
@click.option(
    "-n",
    "--comparables_analysis_name",
    type=str,
    help="Name of excel file with Comparables Analysis template",
    default="compare.xlsx",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    help="File with tickers to use for Comparables Analysis",
    default="compare.txt",
)
@click.option(
    "-t",
    "--template_name",
    type=str,
    help="Name of excel sheet with Comparables Analysis template",
    default="Template",
)
def compare(filename, template_name, comparables_analysis_name):
    """
    Comparables analysis
    """
    application.comparables_analysis(filename, template_name, comparables_analysis_name)
    click.echo(f"Wrote to {comparables_analysis_name}")
