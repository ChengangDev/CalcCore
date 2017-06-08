import unittest

import move

class TestMove(unittest.TestCase):
    def test_mv(self):
        mv = move.Move(240)
        for i in range(240):
            mv.push(i)
            self.assertEqual(mv.ma(1), i)
            self.assertEqual(mv.mmax(i + 1), i)
            self.assertEqual(mv.mmin(i + 1), 0)
            self.assertEqual(mv.mmax(1), i)
            self.assertEqual(mv.mmin(1), i)

        self.assertEqual(mv.ma(240), (0 + 239) / 2.0)
        self.assertEqual(mv.ma(240) * 240, mv.msum(240))


if __name__ == '__main__':
    unittest.main()
