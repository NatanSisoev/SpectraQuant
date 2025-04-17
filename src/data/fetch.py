import datetime
import os

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv

load_dotenv()


def fetch():
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))

    request_params = StockBarsRequest(
        symbol_or_symbols=["FF"],
        timeframe=TimeFrame.Minute,
        start=datetime.datetime(2024, 1, 1),
        end=datetime.datetime(2024, 1, 5),
    )

    bars = client.get_stock_bars(request_params)

    return bars.df
