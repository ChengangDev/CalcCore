# -*- coding: utf-8 -*-

import numpy as np
import merge
import fetch
import quantum
from move import move
import pandas as pd


class Observer:
    """

    """
    def __init__(self, interval):
        self._mg = merge.Merge(60, 0)  #60 seconds
        self._mv = move.Move(60)       #60 minutes
        self._rmv = move.RMove(60)
        self._drmv = move.DRMove(60)

    def watch_history_ticks(self, code, date):
        ftch = fetch.Fetcher(code, date)
        cn = quantum.CN('9:30:00')
        df = ftch.get_hist_tick()

        #dfmv = pd.DataFrame(columns=["price", "ma2", "ma5", "ma10"])
        index = []
        dfmv_dict = {"price":[], "ma2":[], "ma5":[], "ma10":[]}

        dfrmv = pd.DataFrame(columns=[])
        dfdrmv = pd.DataFrame(columns=[])

        for i in reversed(df.index):
            time_str = df.loc[i, 'time']
            price = df.loc[i, 'price']
            vulume = df.loc[i, 'volume']
            seconds = cn.get_seconds(time_str)
            if seconds < 0:
                continue
            t = self._mg.reduce_by_count(seconds, price, vulume)
            if t is None:
                continue
            self._mv.push(t[1])
            index.append(t[0])
            dfmv_dict["price"].append(t[1])
            dfmv_dict["ma2"].append(self._mv.ma(2))
            dfmv_dict["ma5"].append(self._mv.ma(5))
            dfmv_dict["ma10"].append(self._mv.ma(10))

            #self._rmv.push(t[1])
            #self._drmv.push(t[1])

        dfmv = pd.DataFrame(data=dfmv_dict, index=index)
        print(dfmv)
        dfmv.plot(y='price', use_index=True)



if __name__ == "__main__":
    ob = Observer(15)
    ob.watch_history_ticks('600895', '2017-06-09')






