import click

from data.fetch import fetch


@click.group()
def data_commands():
    """
    CLI group for data ingestion:
        - fetch
        - validate
        - save

    CLI wrapper for src/data
    """
    pass

@data_commands.command("fetch")
def fetch_command():
    print(fetch())
