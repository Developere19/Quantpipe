import pandas as pd
import pytest

from src.validation import (
    validate_missing_values,
    validate_duplicate_dates,
    validate_ohlc_relationships,
    validate_positive_values,
    validate_market_data,
)

def test_validate_missing_values_accepts_complete_data():
    df = pd.DataFrame({
        "open": [330.19, 331.20],
        "high": [331.76, 333.00],
        "low": [328.35, 329.50],
        "close": [331.34, 332.40],
        "volume": [31413863, 28000000]
    })

    validate_missing_values(df)

def test_validate_missing_values_rejects_missing_data():
    df = pd.DataFrame({
        "open": [330.19, 331.20],
        "high": [331.76, None],
        "low": [328.35, 329.50],
        "close": [331.34, 332.40],
        "volume": [31413863, 28000000]
    })

    with pytest.raises(ValueError, match="Market data contains missing values"):
        validate_missing_values(df)

def test_validate_duplicate_dates_accepts_unique_dates():
    df = pd.DataFrame(
        {
            "close": [331.34, 333.08]
        },
        index=pd.to_datetime(["2026-09-15", "2026-09-14"])
    )

    validate_duplicate_dates(df)

def test_validate_duplicate_dates_rejects_duplicates():
    df = pd.DataFrame(
        {
            "close": [331.34, 332.00]
        },
        index=pd.to_datetime(["2026-09-15", "2026-09-15"])
    )

    with pytest.raises(ValueError, match="Market data contains duplicate dates"):
        validate_duplicate_dates(df)

def test_validate_ohlc_relationships_accepts_valid_prices():
    df = pd.DataFrame({
        "open": [330.00],
        "high": [335.00],
        "low": [328.00],
        "close": [333.00]
    })

    validate_ohlc_relationships(df)


def test_validate_ohlc_relationships_rejects_invalid_prices():
    df = pd.DataFrame({
        "open": [330.00],
        "high": [320.00],
        "low": [328.00],
        "close": [333.00]
    })

    with pytest.raises(
        ValueError,
        match="Market data contains invalid OHLC relationships"
    ):
        validate_ohlc_relationships(df)

def test_validate_positive_values_accepts_valid_data():
    df = pd.DataFrame({
        "open": [330.00],
        "high": [335.00],
        "low": [328.00],
        "close": [333.00],
        "volume": [31413863]
    })

    validate_positive_values(df)


def test_validate_positive_values_rejects_negative_price():
    df = pd.DataFrame({
        "open": [-330.00],
        "high": [335.00],
        "low": [328.00],
        "close": [333.00],
        "volume": [31413863]
    })

    with pytest.raises(ValueError, match="Market data contains invalid prices"):
        validate_positive_values(df)


def test_validate_positive_values_rejects_negative_volume():
    df = pd.DataFrame({
        "open": [330.00],
        "high": [335.00],
        "low": [328.00],
        "close": [333.00],
        "volume": [-100]
    })

    with pytest.raises(ValueError, match="Market data contains invalid volume"):
        validate_positive_values(df)

def test_validate_market_data_accepts_valid_data():
    df = pd.DataFrame(
        {
            "open": [330.00, 331.00],
            "high": [335.00, 336.00],
            "low": [328.00, 329.00],
            "close": [333.00, 334.00],
            "volume": [31413863, 28000000]
        },
        index=pd.to_datetime(["2026-09-15", "2026-09-14"])
    )

    validate_market_data(df)