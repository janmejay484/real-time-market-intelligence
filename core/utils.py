# =========================
# ALLOWED COMPANIES (FROM COLAB)
# =========================
ALLOWED_COMPANIES = [
    "NETFLIX", "APPLE", "TESLA", "GOOGLE", "MICROSOFT",
    "TCS", "INFOSYS", "RAKUTEN",
    "BITCOIN", "ETHEREUM", "DOGECOIN", "SOLANA",
    "AMAZON", "META", "NVIDIA", "AMD", "INTEL",
    "JP MORGAN", "GOLDMAN SACHS", "MASTERCARD", "VISA",
    "RELIANCE", "HDFC", "ICICI", "WIPRO", "HCL",
    "ADANIPORTS", "ADANIENT", "TATA MOTORS", "MARUTI",
    "COCA COLA", "PEPSICO", "WALMART"
]

# =========================
# COMPANY → YAHOO FINANCE TICKER MAP
# =========================
TICKER_MAP = {
    # Tech
    "NETFLIX": "NFLX",
    "APPLE": "AAPL",
    "TESLA": "TSLA",
    "GOOGLE": "GOOGL",
    "MICROSOFT": "MSFT",
    "AMAZON": "AMZN",
    "META": "META",
    "NVIDIA": "NVDA",
    "AMD": "AMD",
    "INTEL": "INTC",

    # Indian Stocks (NSE)
    "TCS": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFC": "HDFCBANK.NS",
    "ICICI": "ICICIBANK.NS",
    "WIPRO": "WIPRO.NS",
    "HCL": "HCLTECH.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "ADANIENT": "ADANIENT.NS",
    "TATA MOTORS": "TATAMOTORS.NS",
    "MARUTI": "MARUTI.NS",

    # Finance (US)
    "JP MORGAN": "JPM",
    "GOLDMAN SACHS": "GS",
    "MASTERCARD": "MA",
    "VISA": "V",

    # FMCG / Retail
    "COCA COLA": "KO",
    "PEPSICO": "PEP",
    "WALMART": "WMT",

    # Crypto
    "BITCOIN": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "DOGECOIN": "DOGE-USD",
    "SOLANA": "SOL-USD",

    # Others
    "RAKUTEN": "RKUNY"
}

# =========================
# VALIDATION
# =========================
def validate_company(company: str):
    if not company:
        return None
    company = company.strip().upper()
    return company if company in ALLOWED_COMPANIES else None

# =========================
# TICKER RESOLUTION (SAFE)
# =========================
def get_ticker(company: str) -> str | None:
    """
    Returns a Yahoo Finance compatible ticker.
    Never raises exception.
    """
    if not company:
        return None

    company = company.upper()
    return TICKER_MAP.get(company)
