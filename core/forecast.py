from prophet import Prophet
import pandas as pd

def run_prophet(df, days=7):
    """
    Runs Prophet forecast.
    Falls back gracefully if data is insufficient.
    """

    if df is None or len(df) < 60:
        return None   # still safe

    data = df.reset_index()[["Date", "Close"]]
    data.columns = ["ds", "y"]

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    model.fit(data)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(days)
