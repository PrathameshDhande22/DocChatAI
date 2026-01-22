import logging
import sys

_LOGGER_NAME = "DocChatAI"


def setup_logger(level=logging.DEBUG):
    """
    Setup logger once. Safe to call multiple times.
    """
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - Func: %(funcName)s - LineNo: %(lineno)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger


def get_logger() -> logging.Logger:
    """Reuse the same logger everywhere."""
    return logging.getLogger(_LOGGER_NAME)
