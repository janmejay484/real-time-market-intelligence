import yfinance as yf
from core.utils import get_ticker

def fetch_market_data(company):
    ticker = get_ticker(company)

    df = yf.download(
        ticker,
        period="1y",
        progress=False,
        auto_adjust=True
    )

    if df is None or df.empty:
        return None

    # 🔥 FIX: Flatten MultiIndex columns
    if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
        df.columns = [col[0] for col in df.columns]

    return df
