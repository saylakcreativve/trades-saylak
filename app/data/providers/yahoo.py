from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from app.data.providers.base import MarketDataProvider, MarketSnapshot


class YahooProvider(MarketDataProvider):
    name = "Yahoo Finance"

    async def history(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        def fetch() -> pd.DataFrame:
            df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df.dropna(how="all")
        return await asyncio.to_thread(fetch)

    async def snapshot(self, symbol: str) -> MarketSnapshot:
        df = await self.history(symbol, period="5d", interval="1d")
        if df.empty:
            raise ValueError(f"No market data for {symbol}")
        close = float(df["Close"].dropna().iloc[-1])
        change = None
        closes = df["Close"].dropna()
        if len(closes) >= 2:
            change = (close / float(closes.iloc[-2]) - 1.0) * 100
        ts = df.index[-1]
        if hasattr(ts, "to_pydatetime"):
            ts = ts.to_pydatetime()
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return MarketSnapshot(symbol=symbol.upper(), price=close, change_pct=change, timestamp=ts, source=self.name, freshness="DELAYED")

    async def fundamentals(self, symbol: str) -> dict:
        def fetch() -> dict:
            return yf.Ticker(symbol).info
        return await asyncio.to_thread(fetch)
