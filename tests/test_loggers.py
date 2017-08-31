import re
from io import StringIO

from lager.handlers import StreamHandler
from lager.levels import LogLevel
from lager.loggers import Logger


DEFAULT_TEMPLATE_PATTERN = re.compile(
    '(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}) '
    '(?P<level>[A-Z]+) '
    '(?P<name>\w+): '
    '(?P<message>.*)'
)


class TestLogger:
    def setup_method(self, mtd):
        self.stream = StringIO()
        self.handler = StreamHandler(stream=self.stream, level=LogLevel.debug)
        self.logger = Logger(
            name='test', handlers=[self.handler]
        )

    def test_debug(self):
        entry = 'hello'
        self.logger.debug(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert DEFAULT_TEMPLATE_PATTERN.match(output)

    def test_info(self):
        entry = 'hello'
        self.logger.info(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert DEFAULT_TEMPLATE_PATTERN.match(output)

    def test_warning(self):
        entry = 'hello'
        self.logger.warning(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert DEFAULT_TEMPLATE_PATTERN.match(output)

    def test_error(self):
        entry = 'hello'
        self.logger.error(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert DEFAULT_TEMPLATE_PATTERN.match(output)

    def test_capture_exception(self):
        try:
            1 / 0
        except ZeroDivisionError:
            self.logger.capture_exception()
        self.stream.seek(0)
        output = self.stream.getvalue()

        match = DEFAULT_TEMPLATE_PATTERN.match(output)
        assert match

        message = match.groupdict()['message']
        assert message.startswith('Traceback')

    def test_setting_timezone(self):
        self.logger.timezone = 'America/Chicago'

        entry = 'hello'
        self.logger.debug(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        match = DEFAULT_TEMPLATE_PATTERN.match(output)
        assert match

        time = match.groupdict()['time']
        # damn you, daylight savings!
        assert time.endswith('-06:00') or time.endswith('-05:00')

    def test_setting_custom_template(self):
        self.logger.template = '{module}: {message}'

        entry = 'hello'
        self.logger.debug(entry)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert output == 'test_loggers: hello'

    def test_get_kwargs(self):
        kwargs = self.logger._get_kwargs()
        assert all([
            x in kwargs and kwargs[x] is not None
            for x in
            ['name', 'time', 'source', 'function', 'line', 'module', 'pid']
        ])

    def test_provide_context_static_value(self):
        self.logger.template = '{time}: {message}'
        self.logger.debug('hello', time='now')
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert output == 'now: hello'

    def test_provide_context_functional_value(self):
        def get_time():
            return 'now'

        self.logger.template = '{time}: {message}'
        self.logger.debug('hello', time=get_time)
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert output == 'now: hello'

    def test_provide_context_for_non_canonical_key(self):
        self.logger.template = '{derp}: {message}'
        self.logger.debug('hello', derp='ohai')
        self.stream.seek(0)
        output = self.stream.getvalue()

        assert output == 'ohai: hello'
g
