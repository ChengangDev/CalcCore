# -*- coding: utf-8 -*-

from datetime import datetime
import time
import merge
import fetch
import quantum
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
        ftch = fetch.Fetcher(code, date)
        cn = quantum.CN('9:30:00')
        df = ftch.get_hist_tick()
        afternoon = cn.get_seconds('13:00:00')
        offset = cn.get_seconds('11:00:00')

        pivot = fetch.Fetcher.get_pivot(code, date)
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

        self._pivot = fetch.Fetcher.get_pivot(code, date)
        self._rmv = move.RMove(self._pivot, 80) # calc 20 minutes
        self._mg = merge.Merge(15)       # merge 15 seconds into 1

        self._index = []
        self._rmv_dict = {"ma15": [], "diff30": [], "diff60": [], "diff120": [], "diff300": []}

    def __feed(self, dict):
        time_str = dict['time']
        price = dict['price']
        volume = dict['volume']
        seconds = self._quant.time_to_seconds(time_str)
        t = self._mg.reduce(seconds, float(price), int(volume)) # remove duplicate and merge
        if t is None:
            return False

        self._rmv.push(t['avg'])

        self._index.append(t['index'])
        self._rmv_dict["ma15"].append(self._rmv.t_minus(0))
        self._rmv_dict["diff30"].append(self._rmv.t_minus(0) - self._rmv.t_minus(1))
        self._rmv_dict["diff60"].append(self._rmv.t_minus(0) - self._rmv.t_minus(3))
        self._rmv_dict["diff120"].append(self._rmv.t_minus(0) - self._rmv.t_minus(7))
        self._rmv_dict["diff300"].append(self._rmv.t_minus(0) - self._rmv.t_minus(19))

        return True

    def __catch_cliff(self):
        diff300 = self._rmv_dict["diff300"][-1]
        if diff300 > 0.01 or diff300 < -0.01:
            seconds = self._index[-1] * 15  # merge interval
            time_str = self._quant.seconds_to_time(seconds)
            ratio = self._rmv_dict["ma15"][-1]
            print("Catch Cliff: {} {} {} {}".format(self._code, time_str, diff300, ratio))


    def start(self, fetch_interval = 3):
        print("Start observing Cliffs:", self._code)
        self.__init__(self._code)

        while(True):
            dict = fetch.Fetcher.get_realtime_deal(self._code)
            print(datetime.now(), end=' ', flush=False)
            print(dict)
            if self.__feed(dict):
                self.__catch_cliff()
            time.sleep(fetch_interval)

    def simulate(self, date='', fetch_interval=3):
        self.__init__(self._code, date)
        print("Simulate observing Cliffs:", self._code, self._date)

        df = fetch.Fetcher.get_hist_tick(self._code, self._date)
        for i in reversed(df.index):
            dict = {
                "time": df.loc[i, 'time'],
                "code": self._code,
                "price": df.loc[i, "price"],
                "volume": df.loc[i, 'volume'],
             }
            #print(datetime.now(), end=' ', flush=False)
            #print(dict)
            if self.__feed(dict):
                self.__catch_cliff()
            time.sleep(fetch_interval)

    def show(self):
        df = pd.DataFrame(data=self._rmv_dict, index=self._index)
        #print(df)
        axis_y = df.plot()
        # axis_y.set_ylim(-0.1, 0.1)
        plt.show()



if __name__ == "__main__":
    ob = Observer(30)
    #ob.watch_history_ticks('600004', '2017-06-12')
    #ob.watch_history_ticks('002415', '2017-06-12')
    #ob.watch_history_ticks('000858', '2017-06-12')
    ob = CliffObserver('600988', '2017-06-14')
    ob.simulate(fetch_interval=0)
    ob.show()
    #ob.review('000858', '2017-06-14')
    #ts.get_realtime_quotes('000858')







