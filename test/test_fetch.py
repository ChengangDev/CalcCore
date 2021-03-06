import unittest
from operate import fetch

class MyTestCase(unittest.TestCase):
    def test_something(self):

        self.assertEqual(fetch.Fetch.get_pivot('002415', '2017-06-11'), None)
        self.assertEqual(fetch.Fetch.get_pivot('002415', '2017-06-9'), 29.56)
        self.assertEqual(fetch.Fetch.get_pivot('300104', '2017-06-9'), None)

if __name__ == '__main__':
    unittest.main()
