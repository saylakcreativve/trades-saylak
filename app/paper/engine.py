from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class PaperOrder:
    symbol: str
    direction: str
    entry: float
    quantity: float
    stop: float | None = None
    target: float | None = None
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PaperBroker:
    def __init__(self) -> None:
        self.enabled = True
        self.orders: list[PaperOrder] = []

    def submit(self, order: PaperOrder) -> PaperOrder:
        self.orders.append(order)
        return order
