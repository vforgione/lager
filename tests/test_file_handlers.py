import codecs
import os

from lager.enums import Verbosity
from lager.handlers import FileHandler


class TestFileHandler:
    def setup_method(self, mtd):
        self.filename = '/tmp/test_file_handler.log'
        self.handler = FileHandler(self.filename)

    def teardown_method(self, mtd):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_write_entry(self):
        entry = 'Hello, world!'

        self.handler.write_entry(entry, verbosity=Verbosity.info)
        with codecs.open(self.filename, 'r', encoding='utf8') as fh:
            output = [line for line in fh]

        assert output == [entry]

    def test_write_entry_non_ascii(self):
        entry = '안녕하세요'

        self.handler.write_entry(entry, verbosity=Verbosity.info)
        with codecs.open(self.filename, 'r', encoding='utf8') as fh:
            output = [line for line in fh]

        assert output == [entry]
