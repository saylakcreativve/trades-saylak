from __future__ import annotations

import pandas as pd


def ema_signal(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.Series:
    fast_ema = df["Close"].ewm(span=fast, adjust=False).mean()
    slow_ema = df["Close"].ewm(span=slow, adjust=False).mean()
    return (fast_ema > slow_ema).astype(int)
