import inspect
import os
import sys
import traceback
from typing import List, Optional

import arrow

from lager.enums import Verbosity
from lager.handlers import Handler, StdOutHandler


BASE_TEMPLATE_KEYS: List[str] = [
    'name',
    'time',
    'verbosity',
    'message',
    'source',
    'function',
    'line',
    'module',
    'pid',
]


DEFAULT_TEMPLATE: str = '{time} {verbosity} {name}: {message}'


class Logger:
    """``Logger`` is the main interface to create log entries.
    
    This can be as simple or complex as you want it to be. At it's core, all
    this does is string interpolation and then delegates the writes to the
    various handlers attached to it.
    
    The interpolation can be extended beyond the given base template keys by
    adding additional keys to the template and injecting them at write time
    as additional kwargs (see examples below).
    
    .. example::
    >>> from lager import Logger
    >>> logger = Logger('example')
    >>> logger.info('this is an info message')
    2017-09-02T00:54:35.152847+00:00 INFO example: this is an info message
    >>> logger.warning('this is a warning message')
    2017-09-02T00:54:51.208424+00:00 WARNING example: this is a warning message
    >>> logger.error('this is an error message')
    2017-09-02T00:55:04.791726+00:00 ERROR example: this is an error message
    >>> try:
    ...     1 / 0
    ... except ZeroDivisionError:
    ...     logger.capture_exception()
    ...
    2017-09-02T00:57:23.742396+00:00 EXCEPTION example: Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    ZeroDivisionError: division by zero

    .. example::
    >>> template = '{time} {verbosity} {name} {info}: {message}'
    >>> logger = Logger('example', template=template)
    >>> logger.info('got it... thanks', info=':hooray:')
    2017-09-02T01:08:41.546999+00:00 INFO example :hooray:: got it... thanks

    .. example::
    >>> import arrow
    >>> def beer_o_clock() -> str:
    ...     now = arrow.utcnow().to('America/Chicago')
    ...     if now.hour > 17:  # gotta have some standards
    ...             return ':beers:'
    ...     else:
    ...             return 'not yet'
    ...
    >>> template = '{time} {verbosity} {name} {beer}: {message}'
    >>> logger = Logger('example', template=template)
    >>> logger.info('hooray!', beer=beer_o_clock)
    2017-09-02T01:06:24.017288+00:00 INFO example :beers:: hooray!
    """

    def __init__(
            self,
            name: str,
            template: Optional[str]=None,
            timezone: Optional[str]=None,
            handlers: Optional[List[Handler]]=None,
            ensure_new_line: Optional[bool]=True) -> None:
        """Instantiates a new ``Logger``.
        
        :param name: the name of the logger
        :param template: the template for log entries this logger creates
        :param timezone: the local timezone
        :param handlers: handlers used to write the log entries
        :param ensure_new_line: should log entries end with a new line
        """
        self.name: str = name
        self.template: str = template or DEFAULT_TEMPLATE
        self.timezone: str = timezone
        self.handlers: List[Handler] = handlers or [StdOutHandler()]
        self.ensure_new_line: bool = ensure_new_line

    def debug(self, message: str, **context) -> None:
        """Create a log entry with a verbosity of **debug**.
        
        :param message: the message to be logged
        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        self._log(Verbosity.debug, message, err=False, **context)

    def info(self, message: str, **context) -> None:
        """Create a log entry with a verbosity of **info**.
        
        :param message: the message to be logged
        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        self._log(Verbosity.info, message, err=False, **context)

    def warning(self, message: str, **context) -> None:
        """Create a log entry with a verbosity of **warning**.
        
        :param message: the message to be logged
        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        self._log(Verbosity.warning, message, err=False, **context)

    def error(self, message: str, **context) -> None:
        """Create a log entry with a verbosity of **error**.
        
        :param message: the message to be logged
        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        self._log(Verbosity.error, message, err=False, **context)

    def capture_exception(self, **context) -> None:
        """When an exception is caught, this will format the traceback and
        use it as the message portion of the log entry.

        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        self._log(Verbosity.exception, message='', err=True, **context)

    def _log(
            self,
            verbosity: Verbosity,
            message: str,
            err: Optional[bool]=False,
            **context) -> None:
        """Gathers kwargs and context and interpolates those values into the
        logger's template to create a log entry.
        
        :param verbosity: the verbosity of the log entry
        :param message: the message portion of the log entry
        :param err: was an error caught
        :param context: arbitrary key-word values to substitute for 
            template kwargs
        """
        # if an error was caught format it and substitute it for the message
        if err:
            tb = traceback.format_exc()
            message = tb

        # get standard template kwargs, add context values, interpolate template
        kwargs = self._get_kwargs()
        kwargs.update({
            'verbosity': verbosity,
            'message': message,
        })
        run_context = {
            key: value() if callable(value) else value
            for key, value in context.items()
        }
        kwargs.update(run_context)
        entry = self.template.format(**kwargs)

        # make sure the log entry ends with a new line if necessary
        if self.ensure_new_line and not entry.endswith('\n'):
            entry = f'{entry}\n'

        # tell the handlers to write the log entry
        for handler in self.handlers:
            handler.write_entry(entry=entry, verbosity=verbosity)

    def _get_kwargs(self) -> dict:
        """Creates a dictionary of template standard key-word values for
        interpolation and creating the log entry.
        
        Values created::
        
        - ``name``: the name of the logger
        - ``time``: the current timestamp
        - ``source``: full path of the file that called the logging method
        - ``function``: the function name that called the logging method
        - ``line``: the line number of the call to the logging method
        - ``module``: the module name that called the logging method
        - ``pid``: the system process id of the executing code
        
        :return: a dict of key-word values used for interpolation
        """
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
