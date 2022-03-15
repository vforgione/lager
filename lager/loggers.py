from datetime import datetime
from typing import List, Optional, Set

from lager.handlers import Handler
from lager.verbosity import DEBUG, ERROR, INFO, WARNING, Verbosity

class Logger:
    def __init__(
        self,
        handlers: Optional[List[Handler]] = None,
    ) -> None:
        self._template: str = "{time} {verbosity}: {message}"
        self.handlers: Set[Handler] = set(handlers) if handlers else set()

    def debug(self, message: str) -> None:
        self._log(DEBUG, message)

    def info(self, message: str) -> None:
        self._log(INFO, message)

    def warning(self, message: str) -> None:
        self._log(WARNING, message)

    def error(self, message: str) -> None:
        self._log(ERROR, message)

    def _log(self, verbosity: Verbosity, message: str) -> None:
        context = {
            "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "verbosity": str(verbosity),
            "message": message,
        }

        output = self._template.format(**context)
        if not output.endswith("\n"):
            output = f"{output}\n"

        for handler in self.handlers:
            handler.write(output, verbosity)
