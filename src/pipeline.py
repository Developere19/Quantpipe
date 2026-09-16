from src.ingestion import fetch_market_data
from src.validation import validate_market_data
from src.anomaly_detection import detect_anomalies
from src.database import create_market_data_table, insert_market_data
from src.logger import logger


def run_pipeline(symbol: str) -> None:
    """
    Run the complete QuantPipe market data pipeline for a stock symbol.
    """
    logger.info("Starting pipeline for %s", symbol)

    try:
        # Fetch and standardize market data from the external API.
        market_data = fetch_market_data(symbol)

        # Reject invalid data before it reaches downstream systems.
        validate_market_data(market_data)

        # Flag unusual price movements and trading volumes.
        processed_data = detect_anomalies(market_data)

        # Ensure the destination table exists before loading data.
        create_market_data_table()

        # Store the processed data in PostgreSQL.
        insert_market_data(processed_data, symbol)

        logger.info("Pipeline completed successfully for %s", symbol)

    except Exception:
        logger.exception("Pipeline failed for %s", symbol)
        raise


if __name__ == "__main__":
    run_pipeline("AAPL")
