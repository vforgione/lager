from abc import ABCMeta
from io import TextIOWrapper
from os import PathLike
from sys import stderr, stdout
from typing import Protocol, final

from lager.verbosity import INFO, WARNING, Verbosity


class Handler(Protocol):
    def write(self, message: str, verbosity: Verbosity) -> None:
        ...


class StreamHandler(metaclass=ABCMeta):
    def __init__(
        self,
        stream: TextIOWrapper,
        min_verbosity: Verbosity = INFO,
    ) -> None:
        self.stream = stream
        self.min_verbosity = min_verbosity

    def write(self, message: str, verbosity: Verbosity) -> None:
        if self.min_verbosity <= verbosity:
            self.stream.write(message)
            self.stream.flush()


@final
class StdOutHandler(StreamHandler):
    def __init__(self, min_verbosity: Verbosity = INFO) -> None:
        super().__init__(stream=stdout, min_verbosity=min_verbosity)


@final
class StdErrHandler(StreamHandler):
    def __init__(self, min_verbosity: Verbosity = WARNING) -> None:
        super().__init__(stream=stderr, min_verbosity=min_verbosity)


@final
class FileHandler(StreamHandler):
    def __init__(
        self,
        path: PathLike,
        mode: str = "a",
        encoding: str = "utf-8",
        errors: str = "strict",
        buffering: int = 1,
        min_verbosity: Verbosity = INFO,
    ):
        self.fh = open(
            path,
            mode=mode,
            encoding=encoding,
            errors=errors,
            buffering=buffering,
        )
        super().__init__(stream=self.fh, min_verbosity=min_verbosity)

    def __del__(self) -> None:
        self.fh.close()
