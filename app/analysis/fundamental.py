from __future__ import annotations


def fundamental_snapshot(info: dict) -> dict:
    def n(key: str):
        value = info.get(key)
        return float(value) if isinstance(value, (int, float)) else None

    return {
        "revenue_growth": n("revenueGrowth"),
        "earnings_growth": n("earningsGrowth"),
        "gross_margin": n("grossMargins"),
        "operating_margin": n("operatingMargins"),
        "profit_margin": n("profitMargins"),
        "fcf": n("freeCashflow"),
        "debt_to_equity": n("debtToEquity"),
        "current_ratio": n("currentRatio"),
        "roe": n("returnOnEquity"),
        "roic": n("returnOnAssets"),
        "pe": n("trailingPE"),
        "forward_pe": n("forwardPE"),
        "peg": n("pegRatio"),
        "price_to_book": n("priceToBook"),
        "ev_ebitda": n("enterpriseToEbitda"),
        "price_to_sales": n("priceToSalesTrailing12Months"),
    }
