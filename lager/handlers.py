import codecs
import socket
import syslog
from codecs import StreamReaderWriter
from io import TextIOWrapper
from sys import stderr, stdout

from lager.levels import LogLevel


class Handler:

    def write_entry(self, entry: str, level: LogLevel) -> None:
        raise NotImplementedError


class StreamHandler(Handler):

    def __init__(self, stream: TextIOWrapper, level: LogLevel=None) -> None:
        self.stream: TextIOWrapper = stream
        self.level: LogLevel = level or LogLevel.info

    def write_entry(self, entry: str, level: LogLevel) -> None:
        if self.level <= level:
            self.stream.write(entry)


class StdErrHandler(StreamHandler):

    def __init__(self, level: LogLevel=None):
        super().__init__(stream=stderr, level=level)


class StdOutHandler(StreamHandler):

    def __init__(self, level: LogLevel=None):
        super().__init__(stream=stdout, level=level)


class FileHandler(Handler):

    def __init__(
            self,
            fname: str,
            mode: str='a',
            encoding: str='utf8',
            errors: str='strict',
            buffering: int=1,
            level: LogLevel=None) -> None:

        self.fh: StreamReaderWriter = codecs.open(
            filename=fname, mode=mode, encoding=encoding, errors=errors,
            buffering=buffering)
        self.level: LogLevel = level or LogLevel.info
        self.encoding: str = encoding

    def write_entry(self, entry: str, level: LogLevel) -> None:
        if self.level <= level:
            self.fh.write(bytes(entry, self.encoding).decode(self.encoding))
            self.fh.flush()


class SocketHandler(Handler):

    def __init__(self, level: LogLevel=None, **kwargs):
        self.level: LogLevel = level or LogLevel.info
        self.host: str = kwargs.get('host')
        self.port: str = kwargs.get('port')
        self.encoding: str = kwargs.get('encoding', 'utf8')
        self.family: int = kwargs.get('family')
        self.type: int = kwargs.get('type')

        if self.port is not None and self.type != socket.SOCK_DGRAM:
            sock = socket.create_connection((self.host, self.port))
        else:
            if self.port:
                address = (self.host, self.port)
            else:
                address = self.host

            if self.family and self.type:
                sock = socket.socket(self.family, self.type)
            elif self.type:  # NOQA
                sock = socket.socket(socket.AF_UNIX, self.type)
                self.family = socket.AF_UNIX
            else:  # NOQA
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.family = socket.AF_UNIX
                self.type = socket.SOCK_DGRAM

            sock.connect(address)
        self.socket: socket.socket = sock

    def write_entry(self, entry: str, level: LogLevel) -> None:
        if self.level <= level:
            self.socket.sendall(bytes(entry, self.encoding))


class TcpHandler(SocketHandler):

    def __init__(
            self,
            host: str,
            port: int,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        super().__init__(
            level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_STREAM, encoding=encoding)


class TcpIPv6Handler(SocketHandler):

    def __init__(
            self,
            host: str,
            port: int,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        super().__init__(
            level=level, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_STREAM, encoding=encoding)


class UdpHandler(SocketHandler):

    def __init__(
            self,
            host: str,
            port: int,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        super().__init__(
            level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)


class UdpIPv6Handler(SocketHandler):

    def __init__(
            self,
            host: str,
            port: int,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        super().__init__(
            level=level, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_DGRAM, encoding=encoding)


class UnixSocketHandler(SocketHandler):

    def __init__(
            self,
            node: str,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        super().__init__(
            level=level, host=node, family=socket.AF_UNIX,
            type=socket.SOCK_DGRAM, encoding=encoding)


class SyslogHandler(SocketHandler):

    def __init__(
            self,
            facility: int=syslog.LOG_USER,
            host: str='localhost',
            port: int=514,
            encoding: str='utf8',
            level: LogLevel=None) -> None:
        self.facility = facility
        super().__init__(
            level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)

    def write_entry(self, entry: str, level: LogLevel) -> None:
        if self.level <= level:
            priority = self._get_priority(level)
            entry = f'<{priority}>{entry}\000'
            self.socket.sendall(bytes(entry, self.encoding))

    def _get_priority(self, level: LogLevel) -> int:
        """Gets the computed syslog priority value for the priority level.

        :param level: the message's priority value
        :return: the computed syslog priority value

        .. seealso:: https://tools.ietf.org/html/rfc5424
        .. seealso:: http://www.kiwisyslog.com/help/syslog/index.html?protocol_levels.htm
        """
        priority = (self.facility * 8) + level.as_syslog
        return priority
