# core/news_fetcher.py

from __future__ import annotations
import feedparser
import re
import urllib.parse
import logging


def clean(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", text)).strip()


def fetch_news(company: str, limit: int = 12):
    """
    Safe Google News RSS fetcher.
    Handles invalid URLs, encoding issues, and network errors gracefully.
    """
    if not company:
        return []

    try:
        # ✅ URL-safe query
        query = urllib.parse.quote(company.strip())

        url = (
            "https://news.google.com/rss/search?"
            f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        )

        feed = feedparser.parse(url)

        if not feed or not getattr(feed, "entries", None):
            return []

        news = []
        for e in feed.entries[:limit]:
            news.append(
                {
                    "title": clean(getattr(e, "title", "")),
                    "link": getattr(e, "link", "#"),
                    "published": clean(getattr(e, "published", "")),
                    "source": clean(
                        getattr(getattr(e, "source", None), "title", "")
                    ),
                    "description": clean(getattr(e, "summary", "")),
                }
            )

        return news

    except Exception as e:
        # ✅ NEVER crash the app
        logging.warning(f"News fetch failed for {company}: {e}")
        return []
