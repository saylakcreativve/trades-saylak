from __future__ import annotations

import math


def clamp(v: float, lo: float = 0, hi: float = 100) -> float:
    if not math.isfinite(v):
        raise ValueError("Score must be finite")
    return max(lo, min(hi, v))


def technical_score(t: dict) -> float:
    score = 50.0
    trend = t.get("trend")
    score += 15 if trend == "BULLISH" else -15 if trend == "BEARISH" else 0

    macd = t.get("macd")
    if macd is not None:
        score += 10 if macd == "BULLISH" else -10

    rsi = t.get("rsi")
    if rsi is not None:
        rsi = float(rsi)
        score += 8 if 50 <= rsi <= 70 else -5 if rsi > 75 else 3 if 40 <= rsi < 50 else -3

    rv = t.get("rel_volume")
    if rv is not None and float(rv) > 1.5:
        score += 5

    return clamp(score)


def fundamental_score(f: dict) -> float:
    score = 50.0
    for key, weight in [
        ("revenue_growth", 10),
        ("earnings_growth", 10),
        ("gross_margin", 5),
        ("operating_margin", 5),
    ]:
        v = f.get(key)
        if v is not None:
            score += weight if float(v) > 0 else -weight

    pe = f.get("forward_pe")
    if pe is None:
        pe = f.get("pe")
    if pe is not None:
        pe = float(pe)
        score += 5 if 0 < pe < 30 else -5 if pe > 60 else 0

    return clamp(score)


def risk_score(t: dict) -> float:
    hv = t.get("hv20")
    if hv is None:
        return 50.0
    return clamp(75 - float(hv) * 40)


def final_score(components: dict[str, float | None], weights: dict[str, float]) -> float:
    """Weighted score using only available components, normalized to active weights.

    This prevents missing sentiment/macro/geopolitical data from silently becoming
    fake neutral scores and prevents malformed weights from producing invalid totals.
    """
    active: list[tuple[float, float]] = []
    for key, weight in weights.items():
        if weight is None:
            continue
        weight = float(weight)
        if not math.isfinite(weight) or weight < 0:
            raise ValueError(f"Invalid score weight for {key}: {weight}")
        value = components.get(key)
        if value is None:
            continue
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"Invalid component score for {key}: {value}")
        active.append((value, weight))

    total_weight = sum(weight for _, weight in active)
    if total_weight <= 0:
        raise ValueError("No valid score components are available")

    return clamp(sum(value * weight for value, weight in active) / total_weight)
