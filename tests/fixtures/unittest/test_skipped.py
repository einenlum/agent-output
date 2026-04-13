import unittest


class SkippedTest(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_skip(self) -> None:
        self.assertTrue(True)
