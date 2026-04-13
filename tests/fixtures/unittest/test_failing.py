import unittest


class FailingTest(unittest.TestCase):
    def test_fail(self) -> None:
        self.assertEqual(1, 2)
