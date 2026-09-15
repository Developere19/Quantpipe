from src.ingestion import fetch_market_data

def test_fetch_market_data_returns_expected_columns():
    df = fetch_market_data("IBM")

    expected_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    assert list(df.columns) == expected_columns