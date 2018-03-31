import unittest
import option.sina
from datetime import date


class MyTestCase(unittest.TestCase):
    def test_something(self):
        td = date.today()
        months = option.sina.get_trading_months()
        print(months)
        for i in range(6):
            tm = "{0}-{1}".format(td.year, td.month + i)
            day = option.sina.get_trading_expire_day(tm)
            print(day)
        self.assertEqual(len(months), 4)


if __name__ == '__main__':
    unittest.main()
