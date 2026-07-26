"""Application logging setup."""

import logging


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a simple, readable format."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
