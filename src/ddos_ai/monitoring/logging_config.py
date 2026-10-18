"""Logging configuration for console and rotating file logs."""

from pathlib import Path
import logging
import sys


def setup_logging(
    log_file: str = "logs/application/ddos_ai.log",
    level: str = "INFO",
) -> None:
    """Configures root logger with clean formatting and simultaneous file writing."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8"),
    ]

    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers,
        force=True,
    )
