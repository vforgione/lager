from .handlers import StdOutHandler
from .loggers import Logger
from .verbosity import DEBUG

__all__ = [
    "logger",
    "debug",
    "info",
    "warning",
    "error",
]


logger = Logger(handlers=[StdOutHandler(DEBUG)])


def debug(message: str) -> None:
    logger.debug(message)


def info(message: str) -> None:
    logger.info(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)
