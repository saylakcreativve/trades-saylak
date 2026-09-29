from __future__ import annotations


def position_size(capital: float, entry: float, stop: float, risk_per_trade: float, max_position_pct: float) -> dict:
    if capital <= 0 or entry <= 0 or stop <= 0 or entry == stop:
        raise ValueError("Invalid capital/entry/stop")
    risk_amount = capital * risk_per_trade
    risk_per_unit = abs(entry - stop)
    qty = risk_amount / risk_per_unit
    max_qty = (capital * max_position_pct) / entry
    qty = min(qty, max_qty)
    return {"risk_amount": risk_amount, "risk_per_unit": risk_per_unit, "quantity": qty, "notional": qty * entry}
