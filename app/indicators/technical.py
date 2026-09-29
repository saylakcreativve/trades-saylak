from __future__ import annotations

import numpy as np
import pandas as pd


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    c = x["Close"]
    h, l, v = x["High"], x["Low"], x["Volume"]
    for n in [20, 50, 100, 200]:
        x[f"SMA{n}"] = c.rolling(n).mean()
        x[f"EMA{n}"] = c.ewm(span=n, adjust=False).mean()
    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    x["RSI"] = 100 - (100 / (1 + rs))
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    x["MACD"] = ema12 - ema26
    x["MACD_SIGNAL"] = x["MACD"].ewm(span=9, adjust=False).mean()
    x["MACD_HIST"] = x["MACD"] - x["MACD_SIGNAL"]
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    x["ATR"] = tr.rolling(14).mean()
    x["BB_MID"] = c.rolling(20).mean()
    bb_std = c.rolling(20).std()
    x["BB_UPPER"] = x["BB_MID"] + 2 * bb_std
    x["BB_LOWER"] = x["BB_MID"] - 2 * bb_std
    x["BB_WIDTH"] = (x["BB_UPPER"] - x["BB_LOWER"]) / x["BB_MID"]
    x["VOL_SMA20"] = v.rolling(20).mean()
    x["REL_VOLUME"] = v / x["VOL_SMA20"].replace(0, np.nan)
    x["OBV"] = (np.sign(c.diff()).fillna(0) * v).cumsum()
    x["RETURN_20D"] = c.pct_change(20)
    x["HV_20D"] = c.pct_change().rolling(20).std() * np.sqrt(252)
    return x


def support_resistance(df: pd.DataFrame, window: int = 20) -> tuple[float | None, float | None]:
    if len(df) < window:
        return None, None
    recent = df.tail(window)
    return float(recent["Low"].min()), float(recent["High"].max())
