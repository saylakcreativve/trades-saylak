import pandas as pd


def validate_ohlcv(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("DATA UNAVAILABLE")
    if df.index.has_duplicates:
        raise ValueError("Duplicate timestamps in market data")
    if not df.index.is_monotonic_increasing:
        raise ValueError("Market timestamps are not ordered")
    if (df["High"] < df["Low"]).any():
        raise ValueError("Invalid OHLC: high below low")
    if (df["Volume"] < 0).any():
        raise ValueError("Negative volume detected")
