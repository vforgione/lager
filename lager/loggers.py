import inspect
import os
import sys
import traceback
from typing import List

import arrow

from lager.handlers import Handler
from lager.levels import LogLevel


BASE_TEMPLATE_KEYS: List[str] = [
    'name',
    'time',
    'level',
    'message',
    'source',
    'function',
    'line',
    'module',
    'pid',
]


DEFAULT_TEMPLATE = '{time} {level} {name}: {message}'


class Logger:

    def __init__(
            self,
            name: str,
            template: str=None,
            timezone: str=None,
            handlers: List[Handler]=None,
            ensure_new_line: bool=True) -> None:

        self.name: str = name
        self.template: str = template or DEFAULT_TEMPLATE
        self.timezone: str = timezone
        self.handlers: List[Handler] = handlers

        if ensure_new_line and not self.template.endswith('\n'):
            self.template = '{}\n'.format(self.template)

    def debug(self, message: str, **context) -> None:
        self._log(level=LogLevel.debug, message=message, err=False, **context)

    def info(self, message: str, **context) -> None:
        self._log(level=LogLevel.info, message=message, err=False, **context)

    def warning(self, message: str, **context) -> None:
        self._log(level=LogLevel.warning, message=message, err=False, **context)

    def error(self, message: str, **context) -> None:
        self._log(level=LogLevel.error, message=message, err=False, **context)

    def capture_exception(self, **context) -> None:
        self._log(level=LogLevel.debug, message='', err=True, **context)

    def _log(self, level: LogLevel, message: str, err: bool=False, **context):
        if err:
            tb = traceback.format_exc()
            message = tb

        kwargs = self._get_kwargs()
        kwargs.update({
            'level': level,
            'message': message,
        })
        run_context = {
            key: value() if callable(value) else value
            for key, value in context.items()
        }
        kwargs.update(run_context)
        entry = self.template.format(**kwargs)

        for handler in self.handlers:
            handler.write_entry(entry=entry, level=level)

    def _get_kwargs(self) -> dict:
        now = arrow.utcnow()
        if self.timezone and self.timezone != 'UTC':
            now = now.to(self.timezone)

        frame = sys._getframe(3)
        fname, line, func, _, __ = inspect.getframeinfo(frame)
        if func == '<module>':  # NOQA
            func = '__main__'
        module_ = inspect.getmodulename(fname)

        return {  # level and message added in ``_log``
            'name': self.name,
            'time': now,
            'source': fname,
            'function': func,
            'line': line,
            'module': module_,
            'pid': os.getpid(),
        }
