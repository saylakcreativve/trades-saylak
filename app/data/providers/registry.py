from app.data.providers.base import MarketDataProvider
from app.data.providers.yahoo import YahooProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, MarketDataProvider] = {"yahoo": YahooProvider()}

    def get(self, name: str = "yahoo") -> MarketDataProvider:
        return self._providers[name]
