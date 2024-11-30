from lager.handlers import FileHandler, StdErrHandler, StdOutHandler
from lager.loggers import Logger
from lager.verbosity import DEBUG, Verbosity

__all__ = [
    "Logger",
    "FileHandler",
    "StdErrHandler",
    "StdOutHandler",
    "Verbosity",
    "logger",
    "debug",
    "info",
    "warning",
    "error",
]


logger = Logger(handlers=[StdErrHandler(DEBUG)])


def debug(message: str) -> None:
    logger.debug(message)


def info(message: str) -> None:
    logger.info(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)
