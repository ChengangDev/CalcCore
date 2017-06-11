import unittest
from observer import quantum

class MyTestCase(unittest.TestCase):
    def test_something(self):
        cn = quantum.CN('9:30:00')
        self.assertEqual(cn.get_seconds('9:31:5'), 65)


if __name__ == '__main__':
    unittest.main()
