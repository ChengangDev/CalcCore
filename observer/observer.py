# -*- coding: utf-8 -*-

import numpy as np
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
    def __init(self, ob=[]):
        self._ob = ob

    def review(self, code, date):
        ftch = fetch.Fetcher(code, date)
        cn = quantum.CN('9:30:00')
        df = ftch.get_hist_tick()
        afternoon = cn.get_seconds('13:00:00')
        offset = cn.get_seconds('11:00:00')

        pivot = fetch.Fetcher.get_pivot(code, date)
        self._rmv = move.DRMove(pivot, 60)
        self._mg = merge.Merge(15)

        index = []
        dfmv_dict = dfrmv_dict = dfdrmv_dict = {"ma15": [], "diff30": [], "diff60": [], "diff120": [], "diff300": []}

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
            mv = self._rmv

            index.append(t[0])
            dfmv_dict["ma15"].append(mv.ma(1))
            dfmv_dict["diff30"].append(mv.t_minus(0)-mv.t_minus(1))
            dfmv_dict["diff60"].append(mv.t_minus(0)-mv.t_minus(3))
            dfmv_dict["diff120"].append(mv.t_minus(0)-mv.t_minus(7))
            dfmv_dict["diff300"].append(mv.t_minus(0)-mv.t_minus(19))

            # self._rmv.push(t[1])
            # self._drmv.push(t[1])

        dfmv = pd.DataFrame(data=dfmv_dict, index=index)
        print(len(dfmv.index))
        print(dfmv)
        axis_y = dfmv.plot()
        # axis_y.set_ylim(-0.1, 0.1)
        plt.show()


if __name__ == "__main__":
    ob = Observer(30)
    #ob.watch_history_ticks('600004', '2017-06-12')
    #ob.watch_history_ticks('002415', '2017-06-12')
    #ob.watch_history_ticks('000858', '2017-06-12')
    ob = CliffObserver()
    ob.review('000858', '2017-06-12')







