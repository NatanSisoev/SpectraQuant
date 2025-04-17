import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

def save(df: pd.DataFrame, raw: bool = True, **kwargs):
    # Format dates
    for key in ['start_date', 'end_date']:
        if isinstance(kwargs[key], datetime):
            kwargs[key] = kwargs[key].strftime("%Y-%m-%d")

    # Configure file path
    filedir = Path(os.getenv("DATA_DIR"))
    filename = Path(os.getenv("DATA_FILENAME_FORMAT").format(**kwargs))
    filepath = filedir / ("raw" if raw else "processed") / filename

    logging.info(f"Saving data to {filename}...")

    df.to_csv(filepath)

    return filepath
