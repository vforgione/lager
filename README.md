# lager

Stupid Simple Logging 🍺

## Installation

```bash
pip install git+git://github.com/vforgione/lager@main
```

## Usage

```python
from lager import *


info("My name is Vince.")
# 2022-03-13T21:06:28Z INFO: My name is Vince.

warning("I have a rash...")
# 2022-03-13T21:06:33Z WARNING: I have a rash...

error("And I'm contageous!")
# 2022-03-13T21:06:37Z ERROR: And I'm contageous!

debug("jk lol")
# 2022-03-13T21:06:42Z DEBUG: jk lol
```
