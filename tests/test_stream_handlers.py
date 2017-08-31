import io

from capturer import CaptureOutput

from lager.handlers import StreamHandler, StdErrHandler, StdOutHandler
from lager.levels import LogLevel


class TestStreamHandler:
    def setup_method(self, mtd):
        self.stream = io.StringIO()
        self.handler = StreamHandler(stream=self.stream)

    def test_write_entry(self):
        entry = 'Hello, world!'
        self.handler.write_entry(entry, level=LogLevel.info)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == entry

    def test_write_entry_non_ascii(self):
        entry = '안녕하세요'
        self.handler.write_entry(entry, level=LogLevel.info)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == entry

    def test_write_entry_refuses_level_insufficient(self):
        self.handler.level = LogLevel.exception
        entry = 'Hello, world!'

        self.handler.write_entry(entry, LogLevel.debug)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == ''

        self.handler.write_entry(entry, LogLevel.info)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == ''

        self.handler.write_entry(entry, LogLevel.warning)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == ''

        self.handler.write_entry(entry, LogLevel.error)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == ''


class TestStdOutHandler:
    def setup_method(self, mtd):
        self.handler = StdOutHandler()

    def test_write_entry(self):
        entry = 'Hello, world!'
        with CaptureOutput() as co:
            self.handler.write_entry(entry, level=LogLevel.info)
        output = co.get_text()
        assert output == entry

    def test_write_entry_non_ascii(self):
        entry = '안녕하세요'
        with CaptureOutput() as co:
            self.handler.write_entry(entry, level=LogLevel.info)
        output = co.get_text()
        assert output == entry


class TestStdErrHandler:
    def setup_method(self, mtd):
        self.handler = StdErrHandler()

    def test_write_entry(self):
        entry = 'Hello, world!'
        with CaptureOutput() as co:
            self.handler.write_entry(entry, level=LogLevel.info)
        output = co.get_text()
        assert output == entry

    def test_write_entry_non_ascii(self):
        entry = '안녕하세요'
        with CaptureOutput() as co:
            self.handler.write_entry(entry, level=LogLevel.info)
        output = co.get_text()
        assert output == entry
