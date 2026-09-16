import os
import time

import pandas as pd
import requests

from dotenv import load_dotenv

load_dotenv()

def fetch_with_retry(
    url: str,
    params: dict,
    max_retries: int = 3,
    delay: float = 1.0
):
    """
    Send an HTTP GET request and retry temporary network failures.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            return response

        except requests.RequestException:
            if attempt == max_retries:
                raise

            time.sleep(delay)

def fetch_market_data(symbol: str) -> pd.DataFrame:
    """
    Fetch daily market data for a stock symbol and return it
    as a standardized Pandas DataFrame.
    """

    url = "https://www.alphavantage.co/query"

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY is not configured.")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key 
    }

    response = fetch_with_retry(
    url,
    params
    )

    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(
            f"Market data not found for symbol '{symbol}'. "
            f"API response: {data}"
        )

    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(time_series, orient="index")

    df = df.rename(columns={
    "1. open": "open",
    "2. high": "high",
    "3. low": "low",
    "4. close": "close",
    "5. volume": "volume"
    })

    df.index = pd.to_datetime(df.index)
    df.index.name = "date"

    df = df.astype({
    "open": float,
    "high": float,
    "low": float,
    "close": float,
    "volume": int
    })

    return df

if __name__ == "__main__":
    data = fetch_market_data("IBM")
    print(data.head())
    


