def money(v: float | None) -> str:
    return "N/A" if v is None else f"{v:,.2f}"


def pct(v: float | None) -> str:
    return "N/A" if v is None else f"{v:+.2f}%"


def analysis_text(symbol: str, snapshot: dict, tech: dict, fundamental: dict, components: dict, score: float, decision: str, confidence: str, news: list[dict], risk: dict) -> str:
    news_lines = "\n".join(f"• {n['title'][:120]}" for n in news[:5]) or "• Haber verisi bulunamadı."
    return f"""🟢 {symbol.upper()}\n\nPrice: {money(snapshot['price'])}\nDaily Change: {pct(snapshot.get('change_pct'))}\nMarket Data: {snapshot.get('freshness')}\nSource: {snapshot.get('source')}\n\n📊 TECHNICAL\nTrend: {tech['trend']}\nRSI: {money(tech['rsi'])}\nMACD: {tech['macd']}\nEMA20/50/200: {money(tech['ema20'])} / {money(tech['ema50'])} / {money(tech['ema200'])}\nSupport: {money(tech['support'])}\nResistance: {money(tech['resistance'])}\n\n🏢 FUNDAMENTAL\nRevenue Growth: {pct((fundamental.get('revenue_growth') or 0)*100) if fundamental.get('revenue_growth') is not None else 'N/A'}\nEarnings Growth: {pct((fundamental.get('earnings_growth') or 0)*100) if fundamental.get('earnings_growth') is not None else 'N/A'}\nForward P/E: {money(fundamental.get('forward_pe'))}\n\n📰 NEWS\n{news_lines}\n\n🧮 MODEL SCORE\nTechnical: {components['technical']:.1f}\nFundamental: {components['fundamental']:.1f}\nRisk: {components['risk']:.1f}\nFinal Score: {score:.1f}/100\n\nDecision: {decision}\nConfidence: {confidence}\n\n🛡 RISK\nEntry reference: {money(risk.get('entry'))}\nStop: {money(risk.get('stop'))}\nTarget (2R): {money(risk.get('target'))}\nPosition size @ configured risk: {money(risk.get('quantity'))}\n\nWHY\n• Score is a model assessment, not a probability.\n• Current trend/momentum and fundamentals are combined with risk controls.\n• Missing or stale data blocks aggressive signal generation.\n\n⚠️ This is decision support, not guaranteed return or a promise of future performance."""
