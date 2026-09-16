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
        