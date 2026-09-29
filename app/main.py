from __future__ import annotations

import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.bot.app import build_application
from app.config import get_settings
from app.database.db import init_db
from app.utils.logging import setup_logging


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        body = b"OK"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def start_health_server() -> None:
    import os
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()


async def bootstrap() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    await init_db()


def main() -> None:
    start_health_server()
    asyncio.run(bootstrap())
    app = build_application()
    print("SYSTEM READY | Telegram + DB + Market Data")
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
