"""
Logging configuration for error-architecture.

Sets up structured logging with proper formatting and error level output.
"""

import logging
import sys


def configure_logging() -> None:
    """Configure application logging.

    Sets up ERROR level logging with comprehensive formatting including
    timestamps and exception information.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name, typically __name__.

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)
