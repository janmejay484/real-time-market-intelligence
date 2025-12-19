from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
import os
import requests


def build_alert(company: str, ticker: str, counts: dict, *, strategic: dict | None = None):
    """
    Builds a richer alert payload.
    Optionally accepts `strategic` dict: {"competitive_index": float, "strategic_signal": {...}}
    """
    counts = counts or {"positive": 0, "neutral": 0, "negative": 0}

    total = sum(counts.values()) or 1
    pos = counts.get("positive", 0) / total
    neg = counts.get("negative", 0) / total

    # Sentiment label logic
    if pos >= 0.60:
        alert_type = "📈 Bullish Sentiment"
        sentiment_score = round(pos, 2)
        strategic_action = "Consider opportunity: monitor momentum and confirm with forecast."
    elif neg >= 0.60:
        alert_type = "📉 Bearish Sentiment"
        sentiment_score = round(-neg, 2)
        strategic_action = "Risk alert: monitor downside factors and tighten watch on negatives."
    else:
        alert_type = "⚖️ Neutral Sentiment"
        sentiment_score = 0.0
        strategic_action = "Monitor: signals are mixed; wait for confirmation."

    payload = {
        "alert_type": alert_type,
        "company_name": company,
        "company_ticker": ticker,
        "sentiment_score": sentiment_score,
        "sentiment_breakdown": {
            "positive": counts.get("positive", 0),
            "neutral": counts.get("neutral", 0),
            "negative": counts.get("negative", 0),
        },
        "volatility_metric": "Medium",
        "signal_time": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S IST"),
        "strategic_action": strategic_action,
    }

    # Optional strategic layer
    if strategic:
        payload["competitive_index"] = strategic.get("competitive_index")
        payload["strategic_signal"] = strategic.get("strategic_signal")

    return payload


def send_slack(alert: dict) -> bool:
    """
    Sends a human-readable strategic alert message to Slack.
    """
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return False

    breakdown = alert.get("sentiment_breakdown", {})
    strategic_signal = alert.get("strategic_signal", {})

    message = f"""
*{alert.get('alert_type', 'Strategic Alert')}*

*Company:* {alert.get('company_name','')} ({alert.get('company_ticker','')})
*Time:* {alert.get('signal_time','')}

*Market Sentiment Overview*
• Positive News: {breakdown.get('positive', 0)}
• Neutral News: {breakdown.get('neutral', 0)}
• Negative News: {breakdown.get('negative', 0)}

*Strategic Intelligence*
• Competitive Index: {alert.get('competitive_index', 'N/A')} / 100
• Strategic Signal: {strategic_signal.get('signal', 'N/A')}
• Confidence Level: {strategic_signal.get('confidence', 'N/A')}

*Recommended Action*
{alert.get('strategic_action', '')}
"""

    try:
        r = requests.post(
            webhook,
            json={"text": message.strip()},
            timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False


