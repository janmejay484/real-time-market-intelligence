from datetime import datetime
import requests
import os

def build_alert(company, ticker, counts):
    total = sum(counts.values()) or 1
    pos = counts["positive"] / total
    neg = counts["negative"] / total

    if pos > 0.6:
        label = "📈 Bullish Sentiment"
        score = pos
    elif neg > 0.6:
        label = "📉 Bearish Sentiment"
        score = -neg
    else:
        label = "⚖️ Neutral Sentiment"
        score = 0.0

    return {
        "alert_type": label,
        "company_name": company,
        "company_ticker": ticker,
        "sentiment_score": round(score, 2),
        "volatility_metric": "Medium",
        "signal_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategic_action": "Monitor market conditions."
    }

def send_slack(alert):
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return False

    r = requests.post(webhook, json={"text": alert["alert_type"], **alert})
    return r.status_code == 200
