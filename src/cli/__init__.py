import click

from .data import data_commands


@click.group()
def entry():
    """SpectraQuant CLI."""
    pass


entry.add_command(data_commands, "data")  # type: ignore
