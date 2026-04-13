import pytest


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_even(value: int) -> None:
    assert value % 2 == 0
