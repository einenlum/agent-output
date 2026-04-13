import pytest


@pytest.fixture
def broken_fixture():
    raise RuntimeError("boom")


def test_fail_one():
    assert False


def test_fail_two():
    assert 1 == 2


def test_with_error(broken_fixture):
    pass
