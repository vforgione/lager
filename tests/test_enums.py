import syslog

from lager.enums import Verbosity


def test_str():
    assert str(Verbosity.debug) == 'DEBUG'
    assert str(Verbosity.info) == 'INFO'
    assert str(Verbosity.warning) == 'WARNING'
    assert str(Verbosity.error) == 'ERROR'
    assert str(Verbosity.exception) == 'EXCEPTION'


def test_lt():
    assert Verbosity.debug < Verbosity.info < Verbosity.warning < \
           Verbosity.error < Verbosity.exception


def test_le():
    assert Verbosity.debug <= Verbosity.info <= Verbosity.warning <= \
           Verbosity.error <= Verbosity.exception


def test_eq():
    assert Verbosity.debug != Verbosity.info != Verbosity.warning != \
           Verbosity.error != Verbosity.exception


def test_ge():
    assert Verbosity.exception >= Verbosity.error >= Verbosity.warning >= \
           Verbosity.info >= Verbosity.debug


def test_gt():
    assert Verbosity.exception > Verbosity.error > Verbosity.warning > \
           Verbosity.info > Verbosity.debug


def test_as_syslog():
    assert Verbosity.debug.as_syslog == syslog.LOG_DEBUG
    assert Verbosity.info.as_syslog == syslog.LOG_INFO
    assert Verbosity.warning.as_syslog == syslog.LOG_WARNING
    assert Verbosity.error.as_syslog == syslog.LOG_ERR
    assert Verbosity.exception.as_syslog == syslog.LOG_ERR
