import unittest
import option.sina
from datetime import date
import logging

dbgFormatter = "%(levelname)s:%(filename)s:%(lineno)s %(funcName)s() %(message)s"
logging.basicConfig(level=logging.DEBUG, format=dbgFormatter)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        td = date.today()
        months = option.sina.get_trading_months()
        logging.info(months)
        for i in range(3):
            tm = "{0}-{1:02}".format(td.year, td.month + i)
            day = option.sina.get_trading_expire_day(tm)
            logging.info(day)
        self.assertEqual(len(months), 4)

        df = option.sina.get_trading_option_list('510050', months[0])

        df_ohlc = option.sina.get_trading_option_history_ohlc(df.index[0])


if __name__ == '__main__':
    unittest.main()
