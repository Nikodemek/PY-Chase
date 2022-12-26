import logging
from enum import Enum
from logging import Logger


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def configure_logger(log_filepath: str, level: LogLevel):
    logging.basicConfig(
        filename=log_filepath,
        filemode='w',
        level=level.name,
        format="%(asctime)s : %(levelname)s : %(name)s : %(funcName)s : %(message)s"
    )


def get_logger(name: str) -> Logger:
    return logging.getLogger(f"chase.{name}")
