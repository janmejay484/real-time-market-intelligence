import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=False)
def load_finbert():
    return pipeline(
        "sentiment-analysis",
        model="yiyanghkust/finbert-tone",
        tokenizer="yiyanghkust/finbert-tone"
    )

def analyze_sentiment(news_items):
    if not news_items:
        return [], {"positive": 0, "neutral": 1, "negative": 0}

    finbert = load_finbert()

    texts = [n["title"] for n in news_items]
    results = finbert(texts)

    counts = {"positive": 0, "neutral": 0, "negative": 0}
    detailed = []

    for text, r in zip(texts, results):
        label = r["label"].lower()
        counts[label] += 1
        detailed.append({
            "text": text,
            "sentiment": label,
            "confidence": round(r["score"], 3)
        })

    return detailed, counts
