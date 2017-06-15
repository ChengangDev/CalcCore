import unittest
from observer import merge


class MyTestCase(unittest.TestCase):
    def test_merge(self):
        mg = merge.Merge(3)
        self.assertEqual(mg.reduce(0, 1), None)
        self.assertEqual(mg.reduce(1, 2), None)
        self.assertEqual(mg.reduce(None, None), mg.get_snap())
        self.assertEqual(mg.reduce(2, 3), None)
        t = mg.reduce(5, 5)
        self.assertEqual(t["index"], 0)
        self.assertEqual(t["sum"], 6)
        self.assertEqual(t["avg"], 2)
        self.assertEqual(t["open"], 1)
        self.assertEqual(t["close"], 3)
        self.assertEqual(t["min"], 1)
        self.assertEqual(t["max"], 3)

        t = mg.reduce(6, 6)
        self.assertEqual(t["index"], 1)
        self.assertEqual(mg.reduce(None, None)["index"], 2)
        self.assertEqual(mg.reduce(6, 6, 6), None)
        self.assertEqual(mg.reduce(None, None), mg.get_snap())


if __name__ == '__main__':
    unittest.main()
