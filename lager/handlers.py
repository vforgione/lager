import codecs
import socket
import syslog
from codecs import StreamReaderWriter
from io import TextIOWrapper
from sys import stderr, stdout
from typing import Optional

from lager.enums import Verbosity


class Handler:
    """The interface the all *handlers* implement.
    """

    def write_entry(self, entry: str, verbosity: Verbosity) -> None:
        raise NotImplementedError


class StreamHandler(Handler):
    """A generic handler for writing log entries to streams. 
    """

    def __init__(
            self,
            stream: TextIOWrapper,
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``StreamHandler``.
        
        :param stream: the stream object to write to
        :param verbosity: the minimum verbosity of written log entries
        """
        self.stream: TextIOWrapper = stream
        self.verbosity: Verbosity = verbosity or Verbosity.info

    def write_entry(self, entry: str, verbosity: Verbosity) -> None:
        """Write a log entry to the stream.
        
        :param entry: the entry line to be written
        :param verbosity: the verbosity of the log entry
        """
        if self.verbosity <= verbosity:
            self.stream.write(entry)


class StdErrHandler(StreamHandler):
    """A :code:``StreamHandler`` preconfigured to write to ``STDERR``.
    """

    def __init__(self, verbosity: Optional[Verbosity]=None):
        """Instantiates a new ``StdErrHandler``.
        
        :param verbosity: the minimum verbosity of written log entries
        """
        super().__init__(stream=stderr, verbosity=verbosity)


class StdOutHandler(StreamHandler):
    """A :code:``StreamHandler`` preconfigured to write to ``STDOUT``.
    """

    def __init__(self, verbosity: Optional[Verbosity]=None):
        """Instantiates a new ``StdOutHandler``.
        
        :param verbosity: the minimum verbosity of written log entries
        """
        super().__init__(stream=stdout, verbosity=verbosity)


class FileHandler(Handler):
    """A generic handler for writing log entries to files. 
    """

    def __init__(
            self,
            fname: str,
            mode: Optional[str]='a',
            encoding: Optional[str]='utf8',
            errors: Optional[str]='strict',
            buffering: Optional[int]=1,
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``FileHandler``.
        
        :param fname: the path/name of the file to write to
        :param mode: the write mode
        :param encoding: the file encoding
        :param errors: error handling directive
        :param buffering: file buffering directive
        :param verbosity: the minimum verbosity of written log entries
        """
        self.fh: StreamReaderWriter = codecs.open(
            filename=fname, mode=mode, encoding=encoding, errors=errors,
            buffering=buffering)
        self.verbosity: Verbosity = verbosity or Verbosity.info
        self.encoding: str = encoding

    def __del__(self) -> None:  # NOQA
        self.fh.close()

    def write_entry(self, entry: str, verbosity: Verbosity) -> None:
        """Write a log entry to the file.
        
        :param entry: the entry line to be written
        :param verbosity: the verbosity of the log entry
        """
        if self.verbosity <= verbosity:
            self.fh.write(bytes(entry, self.encoding).decode(self.encoding))
            self.fh.flush()


class SocketHandler(Handler):
    """A generic handler for writing log entries to sockets.
    """

    def __init__(self, verbosity: Optional[Verbosity]=None, **kwargs):
        """Instantiates a new ``SocketHandler``.
        
        :param verbosity: the minimum verbosity of the written log entries
        :keyword host: the host portion of the connection -- this can be an 
            FQDN, IP or a local UNIX socket node name
        :keyword port: the port number to connect on
        :keyword encoding: the message encoding
        :keyword family: the socket family -- for example AF_UNIX or AF_INET
        :keyword type: the socket type -- for example SOCK_STREAM or SOCK_DGRAM
        """
        self.verbosity: Verbosity = verbosity or Verbosity.info
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

    def __del__(self) -> None:  # NOQA
        self.socket.close()

    def write_entry(self, entry: str, verbosity: Verbosity) -> None:
        """Write a log entry to the socket.
        
        :param entry: the entry line to be written
        :param verbosity: the verbosity of the log entry
        """
        if self.verbosity <= verbosity:
            self.socket.sendall(bytes(entry, self.encoding))


class TcpHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages over a streaming TCP 
    socket via IPv4.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``TcpHandler``.
        
        :param host: the host portion of the connection -- this can be an 
            FQDN, IP or a local UNIX socket node name
        :param port: the port number to connect on
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        super().__init__(
            verbosity=verbosity, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_STREAM, encoding=encoding)


class TcpIPv6Handler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages over a streaming TCP 
    socket via IPv6.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``TcpIPv6Handler``.
        
        :param host: the host portion of the connection -- this can be an 
            FQDN, IP or a local UNIX socket node name
        :param port: the port number to connect on
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        super().__init__(
            verbosity=verbosity, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_STREAM, encoding=encoding)


class UdpHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages over a UDP 
    socket via IPv4.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``UdpHandler``.
        
        :param host: the host portion of the connection -- this can be an 
            FQDN, IP or a local UNIX socket node name
        :param port: the port number to connect on
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        super().__init__(
            verbosity=verbosity, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)


class UdpIPv6Handler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages over a UDP 
    socket via IPv6.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a new ``UdpIPv6Handler``.
        
        :param host: the host portion of the connection -- this can be an 
            FQDN, IP or a local UNIX socket node name
        :param port: the port number to connect on
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        super().__init__(
            verbosity=verbosity, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_DGRAM, encoding=encoding)


class UnixSocketHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send streaming message to a
    local UNIX socket.
    """

    def __init__(
            self,
            node: str,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a ``UnixSocketHandler``.
        
        :param node: the local UNIX socket
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        super().__init__(
            verbosity=verbosity, host=node, family=socket.AF_UNIX,
            type=socket.SOCK_DGRAM, encoding=encoding)


class SyslogHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send streaming messages to a socket
    formatted as syslog messages.
    """

    def __init__(
            self,
            facility: Optional[int]=syslog.LOG_USER,
            host: Optional[str]='localhost',
            port: Optional[int]=514,
            encoding: Optional[str]='utf8',
            verbosity: Optional[Verbosity]=None) -> None:
        """Instantiates a ``SyslogHandler``.
        
        :param facility: the syslog system to log to
        :param host: the syslog host
        :param port: the syslog port
        :param encoding: the message encoding
        :param verbosity: the minimum verbosity of the written log entries
        """
        self.facility = facility
        super().__init__(
            verbosity=verbosity, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)

    def write_entry(self, entry: str, verbosity: Verbosity) -> None:
        """Write a log entry to the socket formatted as a syslog message.
        
        :param entry: the entry line to be written
        :param verbosity: the verbosity of the log entry
        """
        if self.verbosity <= verbosity:
            priority = self._get_priority(verbosity)
            entry = f'<{priority}>{entry}\000'
            self.socket.sendall(bytes(entry, self.encoding))

    def _get_priority(self, verbosity: Verbosity) -> int:
        """Gets the computed syslog priority value for the priority verbosity.

        :param verbosity: the message's priority value
        :return: the computed syslog priority value

        .. seealso:: https://tools.ietf.org/html/rfc5424
        .. seealso:: http://www.kiwisyslog.com/help/syslog/index.html?protocol_levels.htm
        """
        priority = (self.facility * 8) + verbosity.as_syslog
        return priority
