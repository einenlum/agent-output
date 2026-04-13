import pytest


@pytest.mark.xfail
def test_expected_failure():
    assert False


@pytest.mark.xfail
def test_unexpected_pass():
    assert True
