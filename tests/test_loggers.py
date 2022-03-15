import re
from io import StringIO

from pytest import fixture

from lager.handlers import StreamHandler
from lager.loggers import Logger
from lager.verbosity import DEBUG

time_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"


class _testhandler(StreamHandler):
    def __init__(self):
        super().__init__(StringIO(), DEBUG)


@fixture
def handler() -> StreamHandler:
    return _testhandler()


@fixture
def logger(handler: StreamHandler) -> Logger:
    return Logger(handlers=[handler])


def test_debug(handler: StreamHandler, logger: Logger) -> None:
    logger.debug("Hello, world!")
    output = handler.stream.getvalue()
    assert re.match(rf"{time_pattern} DEBUG: Hello, world!\n", output)


def test_info(handler: StreamHandler, logger: Logger) -> None:
    logger.info("Hello, world!")
    output = handler.stream.getvalue()
    assert re.match(rf"{time_pattern} INFO: Hello, world!\n", output)


def test_warning(handler: StreamHandler, logger: Logger) -> None:
    logger.warning("Hello, world!")
    output = handler.stream.getvalue()
    assert re.match(rf"{time_pattern} WARNING: Hello, world!\n", output)


def test_error(handler: StreamHandler, logger: Logger) -> None:
    logger.error("Hello, world!")
    output = handler.stream.getvalue()
    assert re.match(rf"{time_pattern} ERROR: Hello, world!\n", output)
