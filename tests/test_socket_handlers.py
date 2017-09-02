import os
import socket

from lager.enums import Verbosity
from lager.handlers import SyslogHandler, TcpHandler, TcpIPv6Handler, \
    UdpHandler, UdpIPv6Handler, UnixSocketHandler


class TestSyslogHandler:
    def setup_method(self, mtd):
        self.host = 'localhost'
        self.port = 8514
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        self.handler = SyslogHandler(host=self.host, port=self.port)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        priority = self.handler._get_priority(Verbosity.info)
        msg = '<{}>{}\000'.format(priority, message)
        expected = [bytes(msg, 'utf8')]

        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        priority = self.handler._get_priority(Verbosity.info)
        msg = '<{}>{}\000'.format(priority, message)
        expected = [bytes(msg, 'utf8')]

        assert messages == expected


class TestTcpHandler:
    def setup_method(self, mtd):
        self.host = 'localhost'
        self.port = 8089
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.handler = TcpHandler(host=self.host, port=self.port)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected


class TestTcpIPv6Handler:
    def setup_method(self, mtd):
        self.host = 'localhost'
        self.port = 8089
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.handler = TcpIPv6Handler(host=self.host, port=self.port)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected


class TestUdpHandler:
    def setup_method(self, mtd):
        self.host = 'localhost'
        self.port = 8089
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        self.handler = UdpHandler(host=self.host, port=self.port)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected


class TestUdpIPv6Handler:
    def setup_method(self, mtd):
        self.host = 'localhost'
        self.port = 8089
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        self.handler = UdpIPv6Handler(host=self.host, port=self.port)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected


class TestUnixHandler:
    def setup_method(self, mtd):
        self.node = '/tmp/unix.node'
        if os.path.exists(self.node):
            os.remove(self.node)
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.node)
        self.handler = UnixSocketHandler(node=self.node)

    def teardown_method(self, mtd):
        self.server.close()

    def test_write_entry(self):
        message = 'Hello, world!'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_entry_non_ascii(self):
        message = '안녕하세요'
        self.handler.write_entry(message, verbosity=Verbosity.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected
