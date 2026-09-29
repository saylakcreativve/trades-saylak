from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    price: float
    change_pct: float | None
    timestamp: datetime | None
    source: str
    freshness: str


class MarketDataProvider(ABC):
    name: str

    @abstractmethod
    async def history(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    async def snapshot(self, symbol: str) -> MarketSnapshot:
        raise NotImplementedError

    @abstractmethod
    async def fundamentals(self, symbol: str) -> dict:
        raise NotImplementedError
