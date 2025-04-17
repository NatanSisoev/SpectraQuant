import logging
import os
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from dotenv import load_dotenv

load_dotenv()


def fetch(symbol_or_symbols: str,
          start_date: str | datetime,
          end_date: str | datetime,
          timeframe: str = "1-D",
          adjustment: str = "all",
          feed: str = "iex",
          limit: int = None,
          **kwargs
          ):
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))

    # Timeframe
    r_amount, r_unit = timeframe.split("-")
    amount, unit = int(r_amount), TimeFrameUnit[r_unit.title()]
    timeframe_f = TimeFrame(amount, unit)

    # Request parameters
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol_or_symbols,
        timeframe=timeframe_f,
        start=start_date,
        end=end_date,
        limit=limit,
        adjustment=adjustment,
        feed=feed,
    )

    logging.info(f"Fetching historical stock data with parameters: {request_params}...")

    bars = client.get_stock_bars(request_params)

    return bars.df
