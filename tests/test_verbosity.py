import pytest

from lager.verbosity import DEBUG, ERROR, INFO, WARNING, Verbosity


def test_ordering():
    assert DEBUG < INFO < WARNING < ERROR


@pytest.mark.parametrize(
    ("enum", "expected"),
    [
        (DEBUG, "DEBUG"),
        (ERROR, "ERROR"),
        (INFO, "INFO"),
        (WARNING, "WARNING"),
    ],
)
def test_str(enum: Verbosity, expected: str):
    assert str(enum) == expected
