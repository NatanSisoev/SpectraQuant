import click
from data.fetch import fetch
from data.save import save


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
@click.argument("symbol",     type=click.STRING,   required=True)
@click.argument("start_date", type=click.DateTime(formats=["%Y-%m-%d"]),   required=True)
@click.argument("end_date"  , type=click.DateTime(formats=["%Y-%m-%d"]),   required=True)
@click.argument("timeframe",  type=click.STRING,   required=False, default="1-Day")
@click.argument("adjustment", type=click.STRING,   required=False, default="all")
@click.argument("feed",       type=click.STRING,   required=False, default="iex")
@click.argument("limit",      type=click.INT,      required=False, default=None)
@click.option("--save", "-s", is_flag=True)
def fetch_command(**kwargs):
    df = fetch(**kwargs)

    if df is not None:
        click.echo(df)

    if kwargs["save"]:
        filepath = save(df, raw=True, **kwargs)
        print(filepath)
