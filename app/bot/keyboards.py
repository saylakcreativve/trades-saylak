from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def analysis_keyboard(symbol: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Grafik", callback_data=f"chart:{symbol}"), InlineKeyboardButton("📰 Haberler", callback_data=f"news:{symbol}")],
        [InlineKeyboardButton("⚠️ Riskler", callback_data=f"risk:{symbol}"), InlineKeyboardButton("🧠 Neden?", callback_data=f"why:{symbol}")],
    ])
