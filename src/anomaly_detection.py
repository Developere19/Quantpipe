import pandas as pd


def detect_price_anomalies(
    df: pd.DataFrame,
    threshold: float = 0.10
) -> pd.DataFrame:
    """
    Detect daily closing-price movements that exceed a given threshold.
    """
    result = df.copy()

    result["daily_return"] = result["close"].pct_change()

    result["price_anomaly"] = (
        result["daily_return"].abs() > threshold
    )

    return result

def detect_volume_anomalies(
    df: pd.DataFrame,
    multiplier: float = 2.0
) -> pd.DataFrame:
    """
    Detect trading volume that is unusually high compared with average volume.
    """
    result = df.copy()

    average_volume = result["volume"].mean()

    result["volume_anomaly"] = (
        result["volume"] > average_volume * multiplier
    )

    return result

def detect_anomalies(
    df: pd.DataFrame,
    price_threshold: float = 0.10,
    volume_multiplier: float = 2.0
) -> pd.DataFrame:
    """
    Run all anomaly detection checks on the market data.
    """
    result = detect_price_anomalies(
        df,
        threshold=price_threshold
    )

    result = detect_volume_anomalies(
        result,
        multiplier=volume_multiplier
    )

    return result