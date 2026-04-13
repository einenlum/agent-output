import unittest


class PassingTest(unittest.TestCase):
    def test_one(self) -> None:
        self.assertTrue(True)

    def test_two(self) -> None:
        self.assertTrue(True)
