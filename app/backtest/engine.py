from __future__ import annotations

import pandas as pd


def ema_crossover_backtest(df: pd.DataFrame, fast: int = 20, slow: int = 50, fee_bps: float = 1, slippage_bps: float = 5) -> dict:
    x = df.copy()
    x["fast"] = x["Close"].ewm(span=fast, adjust=False).mean()
    x["slow"] = x["Close"].ewm(span=slow, adjust=False).mean()
    x["signal"] = (x["fast"] > x["slow"]).astype(int)
    x["ret"] = x["Close"].pct_change().fillna(0)
    turnover = x["signal"].diff().abs().fillna(0)
    costs = turnover * ((fee_bps + slippage_bps) / 10000)
    strategy = x["signal"].shift(1).fillna(0) * x["ret"] - costs
    equity = (1 + strategy).cumprod()
    peak = equity.cummax()
    drawdown = equity / peak - 1
    total_return = float(equity.iloc[-1] - 1)
    ann_vol = float(strategy.std() * (252 ** 0.5))
    sharpe = float(strategy.mean() / strategy.std() * (252 ** 0.5)) if strategy.std() else 0.0
    return {"total_return": total_return, "annualized_volatility": ann_vol, "sharpe": sharpe, "max_drawdown": float(drawdown.min()), "trades": int(turnover.sum())}
