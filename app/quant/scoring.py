from __future__ import annotations


def clamp(v: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, v))


def technical_score(t: dict) -> float:
    score = 50.0
    score += 15 if t.get("trend") == "BULLISH" else -15 if t.get("trend") == "BEARISH" else 0
    score += 10 if t.get("macd") == "BULLISH" else -10
    rsi = t.get("rsi")
    if rsi is not None:
        score += 8 if 50 <= rsi <= 70 else -5 if rsi > 75 else 3 if 40 <= rsi < 50 else -3
    rv = t.get("rel_volume")
    if rv and rv > 1.5:
        score += 5
    return clamp(score)


def fundamental_score(f: dict) -> float:
    score = 50.0
    for key, weight in [("revenue_growth", 10), ("earnings_growth", 10), ("gross_margin", 5), ("operating_margin", 5)]:
        v = f.get(key)
        if v is not None:
            score += weight if v > 0 else -weight
    pe = f.get("forward_pe") or f.get("pe")
    if pe is not None:
        score += 5 if 0 < pe < 30 else -5 if pe > 60 else 0
    return clamp(score)


def risk_score(t: dict) -> float:
    hv = t.get("hv20") or 0
    return clamp(75 - hv * 40)


def final_score(components: dict[str, float], weights: dict[str, float]) -> float:
    return clamp(sum(components.get(k, 50.0) * w for k, w in weights.items()))
