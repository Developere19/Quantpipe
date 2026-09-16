from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.database import insert_market_data


@patch("src.database.get_database_connection")
def test_insert_market_data_executes_insert(mock_get_connection):
    """
    Test that processed market data is sent to PostgreSQL.
    """
    mock_connection = Mock()
    mock_cursor = Mock()

    mock_connection.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_connection

    df = pd.DataFrame(
        {
            "open": [100.0],
            "high": [105.0],
            "low": [98.0],
            "close": [103.0],
            "volume": [1000000],
            "daily_return": [0.03],
            "price_anomaly": [False],
            "volume_anomaly": [False],
        },
        index=pd.to_datetime(["2026-09-15"]),
    )

    insert_market_data(df, "AAPL")

    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@patch("src.database.get_database_connection")
def test_insert_market_data_rolls_back_on_failure(mock_get_connection):
    """
    Test that a failed database insert rolls back the transaction.
    """
    mock_connection = Mock()
    mock_cursor = Mock()

    mock_connection.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_connection

    # Simulate PostgreSQL failing during the INSERT.
    mock_cursor.execute.side_effect = Exception("Database insert failed")

    df = pd.DataFrame(
        {
            "open": [100.0],
            "high": [105.0],
            "low": [98.0],
            "close": [103.0],
            "volume": [1000000],
            "daily_return": [0.03],
            "price_anomaly": [False],
            "volume_anomaly": [False],
        },
        index=pd.to_datetime(["2026-09-15"]),
    )

    with pytest.raises(Exception, match="Database insert failed"):
        insert_market_data(df, "AAPL")

    mock_connection.rollback.assert_called_once()
    mock_connection.commit.assert_not_called()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()