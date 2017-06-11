# -*- coding: utf-8 -*-

import numpy as np
import tushare as ts

class Fetcher:
    '''

    '''
    def __init__(self, code, date):
        self._code = code
        self._date = date

    def get_hist_tick(self):
        return ts.get_tick_data(self._code, self._date)


if __name__ == "__main__":
    df = ts.get_tick_data('600848', date='2014-01-09')
    print(df.head(10))