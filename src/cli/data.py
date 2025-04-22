import os
from pathlib import Path

import click
import pandas as pd

from data.fetch import fetch
from data.save import save

# TODO: imports not working


def read_data(filename: str, raw: bool = False):
    filedir = Path(os.getenv("DATA_DIR"))
    filepath = filedir / ("raw" if raw else "processed") / filename

    if not filepath.exists():
        click.secho(f"File: {filepath} does not exist.\nTry --raw or fetch the data first.", fg="red")
        return

    df = pd.read_csv(filepath)

    return df


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
@click.argument("symbol_or_symbols", type=click.STRING, required=True)
@click.argument("start_date", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.argument("end_date", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.argument("timeframe", type=click.STRING, required=False, default="1-Day")
@click.argument("adjustment", type=click.STRING, required=False, default="all")
@click.argument("feed", type=click.STRING, required=False, default="iex")
@click.argument("limit", type=click.INT, required=False, default=None)
@click.option("--save", "-s", is_flag=True)
@click.option("--view", "-v", is_flag=True)
def fetch_command(**kwargs):
    df = fetch(**kwargs)

    if df is not None:
        click.echo(df)

    if kwargs["save"] or kwargs["view"]:
        filepath = save(df, raw=True, **kwargs)
        print(filepath)

        if kwargs["view"]:
            plot_command.main([str(filepath), "--raw"], standalone_mode=False)


@data_commands.command("plot")
@click.argument("filename", type=click.STRING, required=True)
@click.option("--raw", "-r", is_flag=True)
def plot_command(filename: str | Path, **kwargs):
    import plotly.graph_objects as go

    df = read_data(filename, kwargs["raw"])

    # Plot data
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )])
    fig.show()

@data_commands.command("view")
@click.argument("filename", type=click.STRING, required=True)
@click.option("--raw", "-r", is_flag=True)
def view_command(filename: str | Path, **kwargs):
    df = read_data(filename, kwargs["raw"])

    # Print data
    click.echo(df)
