from lager.verbosity import DEBUG, ERROR, INFO, WARNING


def test_ordering():
    assert DEBUG < INFO < WARNING < ERROR
