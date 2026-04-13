import unittest


class ErrorTest(unittest.TestCase):
    def test_error(self) -> None:
        raise ValueError("unexpected error")
