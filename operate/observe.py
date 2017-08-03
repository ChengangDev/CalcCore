# -*- coding: utf-8 -*-

from datetime import datetime
import time

from operate import merge
from . import fetch
from operate import quantum
from move import move
import pandas as pd
import matplotlib.pyplot as plt


class Observer:
    """

    """
    def __init__(self, interval):
        self._interval = interval
        self._mg = merge.Merge(15)  #60 seconds


    def watch_history_ticks(self, code, date):
        ftch = fetch.Fetch(code, date)
        cn = quantum.CN('9:30:00')
        df = ftch.get_hist_tick()
        afternoon = cn.get_seconds('13:00:00')
        offset = cn.get_seconds('11:00:00')

        pivot = fetch.Fetch.get_pivot(code, date)
        self._rmv = move.RMove(pivot, 120)

        index = []
        dfmv_dict = dfrmv_dict = dfdrmv_dict = {"ma15":[],  "mmin60":[], "mmax60":[]}

        for i in reversed(df.index):
            time_str = df.loc[i, 'time']
            price = df.loc[i, 'price']
            vulume = df.loc[i, 'volume']
            seconds = cn.get_seconds(time_str)
            if seconds < 0:
                continue
            if seconds >= afternoon:
                seconds -= offset

            t = self._mg.reduce_by_count(seconds, price, vulume)
            if t is None:
                continue
            self._rmv.push(t[1])
            #self._drmv.push(t[1])
            mv = self._rmv
            #mv = self._drmv

            index.append(t[0])
            dfmv_dict["ma15"].append(mv.ma(1))
            #dfmv_dict["mmin30"].append(mv.mmin(20))
            dfmv_dict["mmin60"].append(mv.mmin(40))
            #dfmv_dict["mmax30"].append(mv.mmax(20))
            dfmv_dict["mmax60"].append(mv.mmax(40))

            #self._rmv.push(t[1])
            #self._drmv.push(t[1])

        dfmv = pd.DataFrame(data=dfmv_dict, index=index)
        #print(dfmv)
        axis_y = dfmv.plot()
        #axis_y.set_ylim(-0.1, 0.1)
        plt.show()


class CliffObserver:
    '''

    '''
    def __init__(self, code, date=''):
        if date == '':
            date = quantum.QuantCN.today()

        self._code = code
        self._date = date

        self._quant = quantum.QuantCN()

        self._pivot = fetch.Fetch.get_pivot(code, date)
        self._rmv = move.RMove(self._pivot, 80)  # calc 20 minutes
        self._mg = merge.Merge(15)       # merge 15 seconds into 1

        self._index = []
        self._rmv_dict = {"diff300": [],}

    def __feed(self, dict):
        time_str = dict['time']
        price = dict['price']
        volume = dict['volume']
        seconds = self._quant.time_to_seconds(time_str)
        t = self._mg.reduce(seconds, float(price), int(volume)) # remove duplicate and merge
        #print(t)
        if t is None:
            return False

        self._rmv.push(price)
        self._index.append(t['index'])
        self._rmv_dict["diff300"].append(self._rmv.t_minus(0) - self._rmv.t_minus(19))

        return True

    def __catch_cliff(self, cliff=0.01):
        diff300 = self._rmv_dict["diff300"][-1]
        seconds = self._mg.expand(self._index[-1])  # merge interval
        time_str = self._quant.seconds_to_time(seconds)

        print("{}: {} diff300 {} ".format(time_str, self._code, diff300))
        if diff300 > cliff or diff300 < -cliff:
            print("Catch Cliff: {} {} {}".format(self._code, time_str, diff300))


    def start(self, fetch_interval = 3):
        print("Start observing Cliffs:", self._code)
        self.__init__(self._code)

        while(True):
            dict = fetch.Fetch.get_realtime_deal(self._code)
            #print(datetime.now(), end=' ', flush=False)
            #print(dict)
            if self.__feed(dict):
                self.__catch_cliff()
            time.sleep(fetch_interval)

    def simulate(self, date='', fetch_interval=3):
        self.__init__(self._code, date)
        print("Simulate observing Cliffs:", self._code, self._date)

        df = fetch.Fetch.get_hist_tick(self._code, self._date)
        for i in reversed(df.index):
            dict = {
                "time": df.loc[i, 'time'],
                "code": self._code,
                "price": df.loc[i, "price"],
                "volume": df.loc[i, 'volume'],
             }
            print(datetime.now(), end=' ', flush=False)
            print(dict)
            if self.__feed(dict):
                self.__catch_cliff()
            time.sleep(fetch_interval)

    def show(self):
        df = pd.DataFrame(data=self._rmv_dict, index=self._index)
        #print(df)
        axis_y = df.plot()
        # axis_y.set_ylim(-0.1, 0.1)
        plt.show()









