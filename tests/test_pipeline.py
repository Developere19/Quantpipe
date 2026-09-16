from unittest.mock import patch

import pytest

from src.pipeline import run_pipeline


@patch("src.pipeline.fetch_market_data")
def test_pipeline_logs_and_raises_failure(mock_fetch_market_data):
    """
    Test that pipeline failures are logged and re-raised.
    """
    mock_fetch_market_data.side_effect = ValueError("API failure")

    with pytest.raises(ValueError, match="API failure"):
        run_pipeline("AAPL")


def test_run_pipeline_calls_all_pipeline_stages():
    """
    Test that the pipeline runs each processing stage in order.
    """
    with (
        patch("src.pipeline.fetch_market_data") as mock_fetch,
        patch("src.pipeline.validate_market_data") as mock_validate,
        patch("src.pipeline.detect_anomalies") as mock_detect,
        patch("src.pipeline.create_market_data_table") as mock_create_table,
        patch("src.pipeline.insert_market_data") as mock_insert
    ):
        mock_market_data = object()
        mock_processed_data = object()

        mock_fetch.return_value = mock_market_data
        mock_detect.return_value = mock_processed_data

        run_pipeline("IBM")

        mock_fetch.assert_called_once_with("IBM")
        mock_validate.assert_called_once_with(mock_market_data)
        mock_detect.assert_called_once_with(mock_market_data)
        mock_create_table.assert_called_once()
        mock_insert.assert_called_once_with(
            mock_processed_data,
            "IBM"
        )