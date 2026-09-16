import pandas as pd


def validate_missing_values(df: pd.DataFrame) -> None:
    """
    Validate that the market data contains no missing values.
    """
    if df.isnull().values.any():
        raise ValueError("Market data contains missing values.")

def validate_duplicate_dates(df: pd.DataFrame) -> None:
    """
    Validate that the market data contains no duplicate trading dates.
    """
    if df.index.duplicated().any():
        raise ValueError("Market data contains duplicate dates.")

def validate_ohlc_relationships(df: pd.DataFrame) -> None:
    """
    Validate that OHLC prices have logically consistent relationships.
    """
    invalid_high = (
        (df["high"] < df["open"]) |
        (df["high"] < df["close"]) |
        (df["high"] < df["low"])
    )

    invalid_low = (
        (df["low"] > df["open"]) |
        (df["low"] > df["close"]) |
        (df["low"] > df["high"])
    )

    if invalid_high.any() or invalid_low.any():
        raise ValueError("Market data contains invalid OHLC relationships.")

def validate_positive_values(df: pd.DataFrame) -> None:
    """
    Validate that prices are positive and volume is non-negative.
    """
    price_columns = ["open", "high", "low", "close"]

    if (df[price_columns] <= 0).any().any():
        raise ValueError("Market data contains invalid prices.")

    if (df["volume"] < 0).any():
        raise ValueError("Market data contains invalid volume.")

def validate_market_data(df: pd.DataFrame) -> None:
    """
    Run all validation checks on the market data.
    """
    validate_missing_values(df)
    validate_duplicate_dates(df)
    validate_positive_values(df)
    validate_ohlc_relationships(df)