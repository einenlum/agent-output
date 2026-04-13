import sys


def test_binary_stdout() -> None:
    sys.stdout.buffer.write(b"\x00\x01\xff")
    sys.stdout.buffer.flush()
    assert True
