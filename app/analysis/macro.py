from __future__ import annotations

from app.data.providers.base import MarketDataProvider


MACRO_SYMBOLS = {"SPY": "^GSPC", "NASDAQ": "^IXIC", "VIX": "^VIX", "DXY": "DX-Y.NYB", "GOLD": "GC=F", "OIL": "CL=F", "US10Y": "^TNX", "BIST100": "XU100.IS"}


async def macro_snapshot(provider: MarketDataProvider) -> dict:
    result: dict[str, dict] = {}
    for name, symbol in MACRO_SYMBOLS.items():
        try:
            s = await provider.snapshot(symbol)
            result[name] = {"price": s.price, "change_pct": s.change_pct, "freshness": s.freshness}
        except Exception:
            result[name] = {"status": "DATA UNAVAILABLE"}
    return result
