from enum import IntEnum


class Verbosity(IntEnum):

    debug = 0
    info = 1
    warning = 2
    error = 3

    def __str__(self) -> str:
        return self.name.upper()

    def __lt__(self, other: "Verbosity") -> bool:
        return self.value < other.value

    def __le__(self, other: "Verbosity") -> bool:
        return self.value <= other.value

    def __eq__(self, other: "Verbosity") -> bool:
        return self.value == other.value

    def __ge__(self, other: "Verbosity") -> bool:
        return self.value >= other.value

    def __gt__(self, other: "Verbosity") -> bool:
        return self.value > other.value


DEBUG = Verbosity.debug

INFO = Verbosity.info

WARNING = Verbosity.warning

ERROR = Verbosity.error
