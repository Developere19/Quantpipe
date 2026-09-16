import logging
import os


def setup_logger() -> logging.Logger:
    """
    Configure and return the QuantPipe application logger.
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("quantpipe")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler("logs/quantpipe.log")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()