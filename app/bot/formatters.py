def money(v: float | None) -> str:
    return "N/A" if v is None else f"{v:,.2f}"


def pct(v: float | None) -> str:
    return "N/A" if v is None else f"{v:+.2f}%"


def analysis_text(
    symbol: str,
    snapshot: dict,
    tech: dict,
    fundamental: dict,
    components: dict,
    score: float,
    decision: str,
    confidence: str,
    news: list[dict],
    risk: dict,
) -> str:
    news_lines = "\n".join(
        f"• {n['title'][:120]}" for n in news[:5]
    ) or "• Haber verisi bulunamadı."

    icon = "🔴" if "BEARISH" in decision else "🟢" if "BULLISH" in decision else "🟡"
    direction = risk.get("direction", "LONG")

    return f"""{icon} {symbol.upper()}

Fiyat: {money(snapshot['price'])}
Günlük Değişim: {pct(snapshot.get('change_pct'))}
Piyasa Verisi: {snapshot.get('freshness')}
Kaynak: {snapshot.get('source')}

📊 TEKNİK
Trend: {tech['trend']}
RSI: {money(tech['rsi'])}
MACD: {tech['macd']}
EMA20/50/200: {money(tech['ema20'])} / {money(tech['ema50'])} / {money(tech['ema200'])}
Destek: {money(tech['support'])}
Direnç: {money(tech['resistance'])}

🏢 TEMEL
Gelir Büyümesi: {pct((fundamental.get('revenue_growth') or 0)*100) if fundamental.get('revenue_growth') is not None else 'N/A'}
Kâr Büyümesi: {pct((fundamental.get('earnings_growth') or 0)*100) if fundamental.get('earnings_growth') is not None else 'N/A'}
Forward P/E: {money(fundamental.get('forward_pe'))}

📰 HABERLER
{news_lines}

🧮 MODEL SKORU
Teknik: {components['technical']:.1f}
Temel: {components['fundamental']:.1f}
Risk: {components['risk']:.1f}
Final Skor: {score:.1f}/100

Karar: {decision}
Güven: {confidence}

🛡 RİSK
Yön: {direction}
Giriş referansı: {money(risk.get('entry'))}
Stop: {money(risk.get('stop'))}
Hedef (2R): {money(risk.get('target'))}
Pozisyon: {money(risk.get('quantity'))}

ℹ️ Notlar
• Skor bir model değerlendirmesidir, olasılık değildir.
• Sentiment, makro ve jeopolitik bileşenler henüz nicel skora dahil edilmemektedir.
• Eksik veya gecikmiş veri agresif sinyal üretimini engeller.
• Bu sistem karar desteğidir; garanti getiri veya kesin tahmin sunmaz."""
