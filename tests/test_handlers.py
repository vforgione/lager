from io import StringIO

from pytest import fixture

from lager.handlers import StreamHandler
from lager.verbosity import DEBUG, INFO


class _testhandler(StreamHandler):
    def __init__(self):
        super().__init__(stream=StringIO(), min_verbosity=INFO)


@fixture
def handler() -> _testhandler:
    return _testhandler()


def test_streamhandler_write(handler: StreamHandler) -> None:
    handler.write("Hello, world!", INFO)
    output = handler.stream.getvalue()
    assert output == "Hello, world!"


def test_streamhandler_enforces_min_verbosity(handler: StreamHandler) -> None:
    handler.write("Hello, world!", DEBUG)
    output = handler.stream.getvalue()
    assert output == ""
