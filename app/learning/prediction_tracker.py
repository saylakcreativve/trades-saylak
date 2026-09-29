from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PredictionRecord:
    prediction_id: str
    timestamp: datetime
    asset: str
    direction: str
    score: float
    probability: float | None
    model_version: str
    features_snapshot: dict


class PredictionTracker:
    """Immutable prediction records. Outcome updates belong to separate result storage."""

    def __init__(self) -> None:
        self.records: list[PredictionRecord] = []

    def record(self, record: PredictionRecord) -> None:
        self.records.append(record)
