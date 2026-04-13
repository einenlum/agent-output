import pytest


@pytest.fixture
def broken_fixture():
    raise RuntimeError("error in fixture setup")


def test_with_error(broken_fixture):
    pass
