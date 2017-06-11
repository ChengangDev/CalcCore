import unittest
from observer import merge


class MyTestCase(unittest.TestCase):
    def test_merge(self):
        mg = merge.Merge(3, 0)
        self.assertEqual(mg.reduce(0, 1), None)
        self.assertEqual(mg.reduce(1, 2), None)
        self.assertEqual(mg.reduce(None, None), (0, 3))
        self.assertEqual(mg.reduce(2, 3), None)

        self.assertEqual(mg.reduce(5, 5), (0, 6))

        self.assertEqual(mg.reduce(6, 6), (1, 5))
        self.assertEqual(mg.reduce(None, None), (2, 6))
        self.assertEqual(mg.reduce(6, 6, 6), None)
        self.assertEqual(mg.reduce_by_count(None, None), (2, 6))


if __name__ == '__main__':
    unittest.main()
