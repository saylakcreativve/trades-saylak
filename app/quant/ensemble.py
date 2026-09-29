from __future__ import annotations


def ensemble_decision(score: float, technical: float, fundamental: float, risk: float) -> tuple[str, str]:
    agreement = max(technical, fundamental) - min(technical, fundamental)
    if risk < 35 or agreement > 35:
        return "HIGH UNCERTAINTY", "LOW"
    if score >= 70:
        return "CONDITIONAL BULLISH", "HIGH" if agreement < 15 else "MEDIUM"
    if score <= 35:
        return "CONDITIONAL BEARISH", "HIGH" if agreement < 15 else "MEDIUM"
    return "WAIT", "MEDIUM"
