from __future__ import annotations

import re

EVENT_RULES = [
    ("WAR", "EXTREME", ["war", "savaş"]),
    ("MILITARY_OPERATION", "HIGH", ["military operation", "askeri operasyon"]),
    ("MISSILE_ATTACK", "HIGH", ["missile", "füze"]),
    ("SANCTIONS", "HIGH", ["sanction", "yaptırım"]),
    ("TRADE_WAR", "HIGH", ["trade war", "ticaret savaşı"]),
    ("CENTRAL_BANK", "MEDIUM", ["fed", "ecb", "central bank", "merkez bankası"]),
    ("INTEREST_RATE", "HIGH", ["interest rate", "faiz"]),
    ("INFLATION", "MEDIUM", ["inflation", "enflasyon", "cpi"]),
    ("ENERGY_SHOCK", "HIGH", ["oil shock", "energy shock", "petrol şoku"]),
    ("BANKING_CRISIS", "EXTREME", ["banking crisis", "bankacılık krizi"]),
]


def classify_event(text: str) -> dict:
    lower = text.lower()
    for event_type, severity, keywords in EVENT_RULES:
        if any(re.search(rf"\b{re.escape(k)}\b", lower) for k in keywords):
            return {"event_type": event_type, "severity": severity, "timeline": "CONFIRMED_EVENT", "confidence": "MEDIUM"}
    return {"event_type": "OTHER", "severity": "LOW", "timeline": "CONFIRMED_EVENT", "confidence": "LOW"}


def scenario_analysis(event: dict) -> dict:
    et = event.get("event_type")
    if et in {"WAR", "MILITARY_OPERATION", "MISSILE_ATTACK", "ENERGY_SHOCK"}:
        return {
            "base": ["Oil supply risk may rise", "Risk premium may increase", "Gold may receive safe-haven demand"],
            "escalation": ["Higher volatility", "Oil upside pressure", "Risk assets may face pressure"],
            "deescalation": ["Risk premium may decline", "Oil shock premium may ease", "Risk assets may stabilize"],
        }
    return {"base": ["Impact is event-specific and requires verification"], "escalation": ["Risk premium may rise"], "deescalation": ["Risk premium may fall"]}
