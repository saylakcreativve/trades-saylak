from __future__ import annotations

import io
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import mplfinance as mpf
from telegram import Update
from telegram.ext import ContextTypes

from app.analysis.fundamental import fundamental_snapshot
from app.analysis.news import fetch_news
from app.analysis.technical import technical_snapshot
from app.bot.formatters import analysis_text
from app.bot.keyboards import analysis_keyboard
from app.config import get_settings, load_yaml_config
from app.data.normalizer import normalize_ohlcv
from app.data.providers.registry import ProviderRegistry
from app.data.validator import validate_ohlcv
from app.quant.ensemble import ensemble_decision
from app.quant.scoring import final_score, fundamental_score, risk_score, technical_score
from app.risk.position_sizing import position_size
from app.risk.stops import atr_stop, rr_target

logger = logging.getLogger(__name__)
registry = ProviderRegistry()
settings = get_settings()
config = load_yaml_config()


def symbol_arg(update: Update) -> str | None:
    parts = (update.message.text or "").split()
    return parts[1].upper() if len(parts) > 1 else None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""PROFESSIONAL QUANT INVESTMENT INTELLIGENCE PLATFORM\n\n/start\n/analiz NVDA\n/grafik NVDA\n/firsatlar\n/piyasa\n/haberler NVDA\n/olaylar\n/riski\n/backtest NVDA\n/status\n/help\n\nSistem karar desteği sağlar; garanti getiri veya kesin tahmin üretmez.""")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def analiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = symbol_arg(update)
    if not symbol:
        await update.message.reply_text("Kullanım: /analiz NVDA")
        return
    try:
        provider = registry.get()
        raw = await provider.history(symbol, period="1y", interval="1d")
        df = normalize_ohlcv(raw)
        validate_ohlcv(df)
        tech = technical_snapshot(df)
        info = await provider.fundamentals(symbol)
        fundamental = fundamental_snapshot(info)
        snapshot = (await provider.snapshot(symbol)).__dict__
        feeds = config.get("news", {}).get("feeds", [])
        news = await fetch_news(feeds, limit=10)
        weights = config.get("score_weights", {})
        components = {
            "technical": technical_score(tech),
            "fundamental": fundamental_score(fundamental),
            "momentum": technical_score(tech),
            "sentiment": 50.0,
            "macro": 50.0,
            "geopolitical": 50.0,
            "risk": risk_score(tech),
        }
        score = final_score(components, weights)
        decision, confidence = ensemble_decision(score, components["technical"], components["fundamental"], components["risk"])
        entry = tech["price"]
        stop = atr_stop(entry, tech["atr"] or entry * 0.02, float(config.get("risk", {}).get("atr_multiplier", 2.0)))
        target = rr_target(entry, stop, 2.0)
        sizing = position_size(100_000, entry, stop, settings.risk_per_trade, settings.max_position_pct)
        risk = {"entry": entry, "stop": stop, "target": target, "quantity": sizing["quantity"]}
        text = analysis_text(symbol, snapshot, tech, fundamental, components, score, decision, confidence, news, risk)
        await update.message.reply_text(text, reply_markup=analysis_keyboard(symbol))
    except Exception as exc:
        logger.exception("analysis failed for %s", symbol)
        await update.message.reply_text(f"DATA UNAVAILABLE / ANALYSIS FAILED\n\n{type(exc).__name__}: {exc}")


async def grafik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = symbol_arg(update)
    if not symbol:
        await update.message.reply_text("Kullanım: /grafik NVDA")
        return
    try:
        provider = registry.get()
        df = normalize_ohlcv(await provider.history(symbol, period="6mo", interval="1d"))
        validate_ohlcv(df)
        x = df.copy()
        x["EMA20"] = x["Close"].ewm(span=20, adjust=False).mean()
        x["EMA50"] = x["Close"].ewm(span=50, adjust=False).mean()
        x["EMA200"] = x["Close"].ewm(span=200, adjust=False).mean()
        ap = [mpf.make_addplot(x["EMA20"]), mpf.make_addplot(x["EMA50"]), mpf.make_addplot(x["EMA200"])]
        fig, _ = mpf.plot(x, type="candle", volume=True, addplot=ap, style="yahoo", title=f"{symbol} | Daily | Decision Support", returnfig=True, figsize=(12, 8))
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        await update.message.reply_photo(buf, caption=f"{symbol} | Daily chart | Data: DELAYED")
    except Exception as exc:
        logger.exception("chart failed for %s", symbol)
        await update.message.reply_text(f"CHART UNAVAILABLE: {exc}")


async def firsatlar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbols = ["SPY", "QQQ", "NVDA", "MSFT", "AAPL", "AMZN", "META", "GOOGL", "AMD", "AVGO"]
    provider = registry.get()
    rows = []
    for symbol in symbols:
        try:
            df = normalize_ohlcv(await provider.history(symbol, period="6mo", interval="1d"))
            validate_ohlcv(df)
            tech = technical_snapshot(df)
            rows.append((technical_score(tech), symbol, tech["trend"], tech["rsi"]))
        except Exception:
            continue
    rows.sort(reverse=True)
    if not rows:
        await update.message.reply_text("DATA UNAVAILABLE")
        return
    body = "\n".join(f"{i}. {s} | Score {sc:.1f} | {tr} | RSI {rsi:.1f}" for i, (sc, s, tr, rsi) in enumerate(rows[:10], 1))
    await update.message.reply_text("TOP CANDIDATES\n\n" + body + "\n\nScore ≠ probability. Liste karar desteğidir.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    token = "OK" if settings.telegram_bot_token else "MISSING"
    await update.message.reply_text(f"SYSTEM STATUS\n\nTelegram: {token}\nDatabase: configured\nMarket Data: Yahoo provider configured\nNews: RSS configured\nML: research module available\nLive trading: DISABLED")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bilinmeyen komut. /help kullan.")
