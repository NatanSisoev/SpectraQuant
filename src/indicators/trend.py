import pandas as pd
import vectorbt as vbt

def simple_moving_average(df: pd.DataFrame) -> pd.DataFrame:
    sma = vbt.MA.run(df['close'], window=20).ma
    df['SMA_20'] = sma
    return df
