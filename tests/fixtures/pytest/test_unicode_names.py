import pytest


def test_café_français() -> None:
    assert True


def test_日本語() -> None:
    assert True


@pytest.mark.parametrize("emoji", ["🚀", "✅", "日本語"])
def test_with_emoji_param(emoji: str) -> None:
    assert isinstance(emoji, str)
