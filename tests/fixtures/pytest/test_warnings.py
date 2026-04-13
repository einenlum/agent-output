import warnings


def test_with_warning():
    warnings.warn("foo", UserWarning)
    assert True
