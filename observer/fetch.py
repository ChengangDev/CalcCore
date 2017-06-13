# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
from datetime import timedelta
import tushare as ts

class Fetcher:
    '''

    '''
    def __init__(self, code, date):
        self._code = code
        self._date = date

    @staticmethod
    def get_pivot(code, date):
        date_object = datetime.strptime(date, '%Y-%m-%d')

        delta = timedelta(days=-1)
        end_object = date_object + delta
        end = end_object.strftime('%Y-%m-%d')

        prev = 14
        for i in range(16):
            delta = timedelta(days=-prev)
            prev *= 2
            start_object = date_object + delta
            start = start_object.strftime('%Y-%m-%d')
            df = ts.get_h_data(code, start, end)

            if df is None or len(df.index) == 0:
                print(start, end)
                continue
            else:
                return df['close'].iloc[0]

        return None

    def get_hist_tick(self):
        return ts.get_tick_data(self._code, self._date)


if __name__ == "__main__":
    print(ts.get_h_data('300104'))