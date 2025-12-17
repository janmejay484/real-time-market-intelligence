import feedparser
import re

def clean(text):
    return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", text)).strip()

def fetch_news(company, limit=8):
    url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(url)

    news = []
    for e in feed.entries[:limit]:
        news.append({
            "title": clean(e.title),
            "link": e.link
        })

    return news
