import pytest
import requests
from unittest.mock import Mock, patch

from src.ingestion import fetch_market_data


@patch("src.ingestion.requests.get")
def test_fetch_market_data_returns_expected_columns(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "Time Series (Daily)": {
            "2026-09-15": {
                "1. open": "330.1900",
                "2. high": "331.7600",
                "3. low": "328.3500",
                "4. close": "331.3400",
                "5. volume": "31413863"
            }
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    df = fetch_market_data("AAPL")

    assert list(df.columns) == [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

@patch("src.ingestion.requests.get")
def test_fetch_market_data_raises_error_for_invalid_response(mock_get):
    mock_response = Mock()

    # Simulate an API response that does not contain market data.
    mock_response.json.return_value = {
        "Information": "API rate limit reached."
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Market data not found"):
        fetch_market_data("AAPL")

@patch("src.ingestion.requests.get")
def test_fetch_market_data_handles_network_failure(mock_get):
    mock_get.side_effect = ConnectionError("Network connection failed")

    with pytest.raises(ConnectionError, match="Network connection failed"):
        fetch_market_data("AAPL")


@patch("src.ingestion.time.sleep")
@patch("src.ingestion.requests.get")
def test_fetch_market_data_retries_after_network_failure(
    mock_get,
    mock_sleep
):
    """
    Test that ingestion retries after a temporary network failure.
    """
    successful_response = Mock()
    successful_response.raise_for_status.return_value = None
    successful_response.json.return_value = {
        "Time Series (Daily)": {
            "2026-09-15": {
                "1. open": "100.00",
                "2. high": "105.00",
                "3. low": "98.00",
                "4. close": "103.00",
                "5. volume": "1000000"
            }
        }
    }

    mock_get.side_effect = [
        requests.ConnectionError("Temporary network failure"),
        successful_response
    ]

    result = fetch_market_data("AAPL")

    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(1.0)
    assert len(result) == 1
    assert result.iloc[0]["close"] == 103.0