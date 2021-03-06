import unittest
from operate import quantum


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qt = quantum.QuantCN()
        print(quantum.QuantCN.today())
        self.assertEqual(qt.time_to_seconds('9:31:5'), 65)
        self.assertEqual(qt.time_to_seconds('11:30:11'), qt.time_to_seconds('13:00:11'))
        self.assertEqual(qt.seconds_to_time(10800), '14:00:00')


if __name__ == '__main__':
    unittest.main()
