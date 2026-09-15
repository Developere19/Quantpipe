import requests
import pandas as pd

def fetch_market_data(symbol: str) -> pd.DataFrame:
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": "demo" 
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

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
    print()
    print(data.dtypes)


