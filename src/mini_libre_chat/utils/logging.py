"""
This file contains the logging utility for each module.
"""

__all__ = ["create_logger"]

import logging


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a custom logger.

    Args:
        name: Name of the logger.
        level: Logging level.

    Returns:
        Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(level)

    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)

    logger.addHandler(c_handler)

    return logger
