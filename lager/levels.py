import syslog
from enum import Enum


class LogLevel(Enum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    exception = 4

    def __str__(self) -> str:
        return self.name.upper()

    def __lt__(self, other: 'LogLevel') -> bool:
        return self.value < other.value

    def __le__(self, other: 'LogLevel') -> bool:
        return self.value <= other.value

    def __eq__(self, other: 'LogLevel') -> bool:
        return self.value == other.value

    def __ge__(self, other: 'LogLevel') -> bool:
        return self.value >= other.value

    def __gt__(self, other: 'LogLevel') -> bool:
        return self.value > other.value

    @property
    def as_syslog(self) -> int:
        if self == LogLevel.debug:
            return syslog.LOG_DEBUG
        elif self == LogLevel.info:
            return syslog.LOG_INFO
        elif self == LogLevel.warning:
            return syslog.LOG_WARNING
        else:
            return syslog.LOG_ERR
