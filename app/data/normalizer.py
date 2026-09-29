from __future__ import annotations

import pandas as pd


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing OHLCV columns: {missing}")
    out = df[required].copy()
    out.index = pd.to_datetime(out.index, utc=True)
    for c in required:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out.dropna(subset=["Open", "High", "Low", "Close"])
