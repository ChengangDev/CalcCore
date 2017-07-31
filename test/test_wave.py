import unittest
from move import wave

class MyTestCase(unittest.TestCase):
    def test_wave(self):
        self.assertEqual(True, True)

    def test_swing(self):
        post = wave.PostSwing()
        prev = wave.PrevSwing()

        post.push(1)
        self.assertEqual(post._q[0], 1)
        post.push(2)
        self.assertEqual(post._q[0], 1)
        self.assertEqual(post._post_min[0], 1)
        self.assertEqual(post._post_max[0], 2)
        post.push(3)
        self.assertEqual(post._q[1], 2)
        self.assertEqual(post._post_min[1], 2)
        self.assertEqual(post._post_min[2], 3)
        self.assertEqual(post._post_max[0], 3)
        self.assertEqual(post._post_max[1], 3)

        prev.push(1)
        self.assertEqual(prev._q[0], 1)
        self.assertEqual(prev._prev_max[0], 1)
        prev.push(2)
        prev.push(3)
        self.assertEqual(prev._prev_max[0], 1)
        self.assertEqual(prev._prev_max[2], 3)
        self.assertEqual(prev._prev_min[0], 1)
        self.assertEqual(prev._prev_min[2], 1)



if __name__ == '__main__':
    unittest.main()
