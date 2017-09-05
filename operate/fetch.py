# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import tushare as ts
import os

class Fetch:
    '''

    '''
    def __init__(self, code, date):
        self._code = code
        self._date = date

    @staticmethod
    def getdir(code):
        path = "/home/ee/data/fetch/" + code
        if os.path.isdir(path) is False:
            os.makedirs(path)
        return path

    @staticmethod
    def get_pivot(code, date, cached=True):
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%Y-%m-%d')
        path = "{0}/hist_{1}_{2}.csv".format(Fetch.getdir(code), code, date)
        df = pd.DataFrame()
        if os.path.isfile(path) and cached:
            print('local data {0}'.format(path))
            df = pd.read_csv(path)
        else:
            print('online data')
            df = ts.get_hist_data(code, date, date)
            df.to_csv(path, index=False)
            #print(df.head(10))

        if df is None or len(df.index) == 0:
            return None
        else:
            return df['close'].iloc[0] - df['price_change'].iloc[0]


    @staticmethod
    def get_hist_tick(code, date, cached=True):
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%Y-%m-%d')
        path = "{0}/tick_{1}_{2}.csv".format(Fetch.getdir(code), code, date)
        df = pd.DataFrame()
        if os.path.isfile(path) and cached:
            print('local data {0}'.format(path))
            df = pd.read_csv(path)
        else:
            print('online data')
            df = ts.get_tick_data(code, date)
            df.to_csv(path, index=False)
        return df

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

    @staticmethod
    def get_price_group(code, date, cached=True):
        date_object = datetime.strptime(date, '%Y-%m-%d')
        date = date_object.strftime('%Y-%m-%d')
        path = "{0}/group_{1}_{2}.csv".format(Fetch.getdir(code), code, date)
        if os.path.isfile(path) and cached:
            print('local group {0}'.format(path))
            df = pd.read_csv(path)
        else:
            print('calc group')
            df = Fetch.get_hist_tick(code, date, cached)
            df = df.groupby('price').sum()
            df.to_csv(path)
        #print(df.head(100))
        return df


if __name__ == "__main__":
    #df = Fetch.get_pivot('', '')
    Fetch.get_price_group('600036', '2017-8-29')




