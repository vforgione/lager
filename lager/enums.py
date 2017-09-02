import syslog
from enum import Enum


class Verbosity(Enum):
    """``Verbosity`` is an enumeration to help control the minimum verbosity
    of logged entries.
    """

    debug = 0
    info = 1
    warning = 2
    error = 3
    exception = 4

    def __str__(self) -> str:
        return self.name.upper()

    def __lt__(self, other: 'Verbosity') -> bool:
        return self.value < other.value

    def __le__(self, other: 'Verbosity') -> bool:
        return self.value <= other.value

    def __eq__(self, other: 'Verbosity') -> bool:
        return self.value == other.value

    def __ge__(self, other: 'Verbosity') -> bool:
        return self.value >= other.value

    def __gt__(self, other: 'Verbosity') -> bool:
        return self.value > other.value

    @property
    def as_syslog(self) -> int:
        """Gets the ``syslog`` priority equivalent of the verbosity.
        """
        if self == Verbosity.debug:
            return syslog.LOG_DEBUG
        elif self == Verbosity.info:
            return syslog.LOG_INFO
        elif self == Verbosity.warning:
            return syslog.LOG_WARNING
        else:
            return syslog.LOG_ERR
