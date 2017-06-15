# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import tushare as ts
import quantum

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

    @staticmethod
    def get_hist_tick(code, date):
        return ts.get_tick_data(code, date)

    @staticmethod
    def get_realtime_deal(code):
        df = ts.get_realtime_quotes(code)
        while(df is None):
            time.sleep(2)
            print('.', end='', flush=True)
            df = ts.get_realtime_quotes(code)

        return {
            "time": df.loc[0, 'time'],
            "name": df.loc[0, 'name'],
            "code": df.loc[0, 'code'],
            "price": df.loc[0, "price"],
            "volume": df.loc[0, 'volume'],
        }


if __name__ == "__main__":
    #ob.review('000858', '2017-06-14')
    df = Fetcher.get_realtime_deal('600895')
    print(df)
