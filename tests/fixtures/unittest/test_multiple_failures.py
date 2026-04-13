import unittest


class MultipleFailuresTest(unittest.TestCase):
    def test_fail_one(self) -> None:
        self.assertEqual(1, 2)

    def test_fail_two(self) -> None:
        self.assertEqual(3, 4)

    def test_error(self) -> None:
        raise RuntimeError("boom")
