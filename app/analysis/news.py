from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser

from app.analysis.geopolitical import classify_event


async def fetch_news(feeds: list[str], limit: int = 20) -> list[dict]:
    def fetch() -> list[dict]:
        items: list[dict] = []
        for url in feeds:
            parsed = feedparser.parse(url)
            for e in parsed.entries[:limit]:
                published = None
                raw = e.get("published") or e.get("updated")
                if raw:
                    try:
                        published = parsedate_to_datetime(raw).astimezone(timezone.utc).isoformat()
                    except Exception:
                        published = raw
                title = e.get("title", "").strip()
                summary = e.get("summary", "").strip()
                event = classify_event(f"{title} {summary}")
                items.append({"title": title, "summary": summary, "source": url, "published_at": published or datetime.now(timezone.utc).isoformat(), "event": event})
        return items
    return await asyncio.to_thread(fetch)
