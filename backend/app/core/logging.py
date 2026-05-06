import logging
import sys
from datetime import datetime


def setup_logging():
    """Configure professional logging for the application"""

    # Format
    log_format = (
        "%(asctime)s | %(levelname)-8s | "
        "%(name)s | %(message)s"
    )

    # Date format
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    # Set levels for noisy libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")

    return logger