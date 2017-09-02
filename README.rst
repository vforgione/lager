=====
lager
=====

Stupid Simple Logging 🍺


------------
Installation
------------

``lager`` is available on PyPI::

.. code-block: bash
   pip install lager

Or if you want to live on the edge::

.. code-block: bash
   pip install git+git://github.com/vforgione/lager@master


Usage
-----

**Major Caveat:** this is written using Python 3.6 annotations - you must
use 3.6 version or better. Why? Because why not?

I strive to reduce complexity, especially when it comes to logging - it should
**Just Work**™️.

Defaults
^^^^^^^^

That being said, there are a couple defaults that I have selected for you::

- *verbosity* is set to ``info``
- a single attached handler that writes entries to ``STDOUT``
- using ISO 8601 formatted timestamps and defaulting to UTC

Hopefully that's agreeable. If not, you're free to change anything and
everything about how this thing works. 🍻

An Example (Finally)
^^^^^^^^^^^^^^^^^^^^

Here's a really stupid simple example (emphasis on stupid)::

.. code-block:: python
   from lager import Logger

   logger = Logger('example')
   logger.info("yay it's working!")

   # 2017-09-02T17:25:35.172228+00:00 INFO example: yay it's working!

   try:
       1 / 0
   except ZeroDivisionError:
       logger.error("that's it -- you're cut off. you just tried to divide by 0!")
       logger.capture_exception()

   # 2017-09-02T17:27:42.105390+00:00 ERROR example: that's it -- you're cut off. you just tried to divide by 0!
   # 2017-09-02T17:27:42.106565+00:00 EXCEPTION example: Traceback (most recent call last):
   #   File "<stdin>", line 2, in <module>
   # ZeroDivisionError: division by zero

Custom Templates
^^^^^^^^^^^^^^^^

If you want to create a custom template, there are a bunch of default available
interpolation keys::

- ``name``: the name of the logger
- ``time``: the current timestamp
- ``verbosity``: the verbosity/priority of the log entry
- ``message``: whatever you want to write in the entry
- ``source``: full path of the file that called the logging method
- ``function``: the function name that called the logging method
- ``line``: the line number of the call to the logging method
- ``module``: the module name that called the logging method
- ``pid``: the system process id of the executing code

All you need to do is create a template string and apply it to the logger::

.. code-block:: python
   from lager import Logger, Verbosity

   template = '{time} {verbosity} {module} {line}: {message}'
   logger = Logger('fires', verbosity=Verbosity.error, template=template)

Incidentally, the above example will create a ``StdOutHandler`` with minimum
verbosity set to *error* and attach it to the logger.

Handlers
^^^^^^^^

You can attach as many handlers as you like. For example, if you wanted an
informational log on disk and errors and exceptions sent to a central logging
server, you could do::

.. code-block:: python
   from lager import FileHandler, Logger, TcpHandler, Verbosity

   info_handler = FileHandler('/var/log/app.log', verbosity=Verbosity=info)
   err_handler = TcpHandler(
      host='https://errors.example.com/', port=9999, verbosity=Verbosity.error)
   logger = Logger('app', handlers=[info_handler, err_handler])


Advanced Usage
--------------

Simple doesn't mean *unconfigurable*.

Let's pretend you have a webapp that assigns each request an id. As events
happen in your stack, you want to log those events and tag them with the id.
Rather than constantly having to remember to add the id to the message, you
could create a custom template and use a function to inject the id into your
log entries::

.. code-block:: python
   from lager import Logger
   from myapp import get_session

   def get_request_id():
      session_info = get_session()
      req_id = session_info.get('req_id')
      return req_id

   template = '{time} {verbosity} {req_id}: {message}'
   logger = Logger('app', additional_context={'req_id', get_request_id})

Now, every log entry will get the current request's id. 🍻

Context can also be injected at write time -- whenever you call ``debug``,
``info``, ``warning``, ``error`` or ``capture_exception`` you can provide
overrides to values for template interpolation.

Here's another stupid example::

.. code-block:: python
   logger.info('this really is not helpful', time='now')

Which will override the default current timestamp value for ``time`` with the
value ``'now'``.
