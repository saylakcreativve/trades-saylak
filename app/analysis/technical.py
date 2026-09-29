from __future__ import annotations

import pandas as pd

from app.indicators.technical import add_indicators, support_resistance


def technical_snapshot(df: pd.DataFrame) -> dict:
    x = add_indicators(df).dropna(how="all")
    row = x.iloc[-1]
    support, resistance = support_resistance(x)
    close = float(row["Close"])
    trend = "BULLISH" if close > float(row["EMA200"]) else "BEARISH" if close < float(row["EMA200"]) else "NEUTRAL"
    macd = "BULLISH" if row["MACD"] > row["MACD_SIGNAL"] else "BEARISH"
    return {
        "price": close,
        "trend": trend,
        "rsi": float(row["RSI"]) if pd.notna(row["RSI"]) else None,
        "macd": macd,
        "macd_hist": float(row["MACD_HIST"]) if pd.notna(row["MACD_HIST"]) else None,
        "ema20": float(row["EMA20"]), "ema50": float(row["EMA50"]),
        "ema100": float(row["EMA100"]), "ema200": float(row["EMA200"]),
        "atr": float(row["ATR"]) if pd.notna(row["ATR"]) else None,
        "rel_volume": float(row["REL_VOLUME"]) if pd.notna(row["REL_VOLUME"]) else None,
        "hv20": float(row["HV_20D"]) if pd.notna(row["HV_20D"]) else None,
        "support": support, "resistance": resistance,
    }
