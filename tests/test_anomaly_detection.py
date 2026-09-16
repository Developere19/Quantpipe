import pandas as pd

from src.anomaly_detection import (
    detect_price_anomalies,
    detect_volume_anomalies,
    detect_anomalies,
)

def test_detect_price_anomalies_ignores_normal_movements():
    df = pd.DataFrame({
        "close": [100.00, 103.00, 105.00]
    })

    result = detect_price_anomalies(df)

    assert result["price_anomaly"].sum() == 0

def test_detect_price_anomalies_flags_large_movement():
    df = pd.DataFrame({
        "close": [100.00, 103.00, 120.00]
    })

    result = detect_price_anomalies(df)

    assert result["price_anomaly"].sum() == 1

def test_detect_volume_anomalies_ignores_normal_volume():
    df = pd.DataFrame({
        "volume": [1000, 1100, 900, 1050]
    })

    result = detect_volume_anomalies(df)

    assert result["volume_anomaly"].sum() == 0


def test_detect_volume_anomalies_flags_unusual_volume():
    df = pd.DataFrame({
        "volume": [1000, 1100, 900, 1000, 5000]
    })

    result = detect_volume_anomalies(df)

    assert result["volume_anomaly"].sum() == 1

def test_detect_anomalies_combines_all_checks():
    df = pd.DataFrame({
        "close": [100.00, 103.00, 120.00, 121.00, 122.00],
        "volume": [1000, 1100, 900, 1000, 5000]
    })

    result = detect_anomalies(df)

    assert "daily_return" in result.columns
    assert "price_anomaly" in result.columns
    assert "volume_anomaly" in result.columns

    assert result["price_anomaly"].sum() == 1
    assert result["volume_anomaly"].sum() == 1

