from app import application
import click


@click.group()
def cli():
    pass


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
    default="tickers",
)
def tickers(filename, ticker_dir):
    """
    Prints tickers in file
    """
    # Print filename with a long line under it
    click.echo(filename)
    click.echo("---------------")
    [click.echo(i) for i in application.get_company_tickers(filename)]


@cli.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    default="load.txt",
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
    default="comparables_analysis.xlsx",
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
    click.echo(f"Wrote to {filename}")
