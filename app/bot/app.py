from __future__ import annotations

import logging

from telegram.ext import Application, CommandHandler

from app.bot.handlers import analiz, firsatlar, grafik, help_command, start, status, unknown
from app.config import get_settings

logger = logging.getLogger(__name__)


def build_application() -> Application:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Put it in .env")
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analiz", analiz))
    app.add_handler(CommandHandler("grafik", grafik))
    app.add_handler(CommandHandler("firsatlar", firsatlar))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("piyasa", status))
    app.add_handler(CommandHandler("riski", status))
    app.add_handler(CommandHandler("backtest", status))
    app.add_handler(CommandHandler("models", status))
    app.add_handler(CommandHandler("performance", status))
    app.add_handler(CommandHandler("paper", status))
    app.add_handler(CommandHandler("olaylar", status))
    app.add_handler(CommandHandler("haberler", status))
    app.add_handler(CommandHandler("detay", analiz))
    app.add_handler(CommandHandler("senaryo", analiz))
    app.add_handler(CommandHandler("unknown", unknown))
    return app
