from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class ModelResult:
    model: Pipeline
    accuracy: float
    brier: float


def train_direction_model(df: pd.DataFrame) -> ModelResult:
    x = df.copy()
    features = [
        c
        for c in ["RSI", "MACD", "MACD_HIST", "ATR", "REL_VOLUME", "HV_20D", "RETURN_20D"]
        if c in x
    ]
    if not features:
        raise ValueError("No valid ML features available")

    # The final row has no known next-day outcome. Do not turn that NaN into class 0.
    next_close = x["Close"].shift(-1)
    x["target"] = (next_close > x["Close"]).astype("float")
    x.loc[next_close.isna(), "target"] = pd.NA
    x = x.dropna(subset=features + ["target"])

    split = int(len(x) * 0.8)
    train, test = x.iloc[:split], x.iloc[split:]
    if len(train) < 50 or len(test) < 10:
        raise ValueError("Insufficient time-series data for ML training")
    if train["target"].nunique() < 2:
        raise ValueError("Training target contains only one class")

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    model.fit(train[features], train["target"].astype(int))
    p = model.predict_proba(test[features])[:, 1]
    pred = (p >= 0.5).astype(int)

    return ModelResult(
        model=model,
        accuracy=float(accuracy_score(test["target"].astype(int), pred)),
        brier=float(brier_score_loss(test["target"].astype(int), p)),
    )
