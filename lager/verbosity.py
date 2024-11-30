from enum import IntEnum


class Verbosity(IntEnum):
    debug = 0
    info = 1
    warning = 2
    error = 3

    def __str__(self) -> str:
        return self.name.upper()


DEBUG = Verbosity.debug

INFO = Verbosity.info

WARNING = Verbosity.warning

ERROR = Verbosity.error
