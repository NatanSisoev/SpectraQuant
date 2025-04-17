import logging
import os
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(level=logging.DEBUG)


def fetch(symbol: str,
          start_date: str | datetime,
          end_date: str | datetime,
          timeframe: str = "1-D",
          adjustment: str = "all",
          feed: str = "iex",
          limit: int = None,
          **kwargs
          ):
    """
    Fetches historical stock data for a given symbol and date range.

    Args:
        symbol_or_symbols: The stock ticker symbol.
        timeframe: The timeframe for the data (e.g., "1-Min", "5-Min", "1-Hour", "1-Day").
        start_date: The starting date in 'YYYY-MM-DD' format.
        end_date: The ending date in 'YYYY-MM-DD' format.
        limit: The maximum number of data points to return.
        adjustment: The adjustment type ('raw', 'split', 'dividend', 'all').
        feed: The data feed to use ('iex', 'sip').

    Returns:
        A pandas DataFrame containing the historical stock data, or None if an error occurs.
    """
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))

    try:
        r_amount, r_unit = timeframe.split("-")

        amount = int(r_amount)
        unit = TimeFrameUnit[r_unit.title()]

        timeframe_f = TimeFrame(amount, unit)

        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe_f,
            start=start_date,
            end=end_date,
            limit=limit,
            adjustment=adjustment,
            feed=feed,
        )
        logging.info(f"Fetching historical stock data with parameters: {request_params}...")
        bars = client.get_stock_bars(request_params).df
        return bars
    except Exception as e:
        logging.error(e)
        return None
