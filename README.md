# lager

Stupid Simple Logging 🍺

## Installation

```bash
uv add https://github.com/vforgione/lager
```

## Usage

Setup a logger with handlers:

```python
from lager import Logger, FileHandler, StdErrHandler, Verbosity

logger = Logger(
    handlers=[
        FileHandler("/path/to/app.log", min_verbosity=Verbosity.DEBUG),
        StdErrHandler(min_verbosity=Verbosity.WARNING),
    ]
)
```

Or you can use the default logger (writes everything to STDERR):

```python
from lager import logger

logger.debug("This is a debug message")
# 2024-11-30T16:55:47+0000 DEBUG: This is a debug message

logger.info("This is an info message")
# 2024-11-30T16:55:36+0000 INFO: This is an info message

warning("This is a warning message")
# 2024-11-30T16:55:39+0000 WARNING: This is a warning message

logger.error("This is an error message")
# 2024-11-30T16:55:44+0000 ERROR: This is an error message
```

Or you can use the default logger's methods directly:

```python
from lager import debug, info, warning, error

debug("This is a debug message")
# 2024-11-30T16:55:47+0000 DEBUG: This is a debug message

info("This is an info message")
# 2024-11-30T16:55:36+0000 INFO: This is an info message

warning("This is a warning message")
# 2024-11-30T16:55:39+0000 WARNING: This is a warning message

error("This is an error message")
# 2024-11-30T16:55:44+0000 ERROR: This is an error message
```
