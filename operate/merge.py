# -*- coding: utf-8 -*-

import numpy as np

class Merge:
    '''

    '''
    def __init__(self, interval):
        self._interval = interval
        self._sum = 0
        self._count = 0
        self._index = 0
        self._last = 0
        self._open = 0
        self._close = 0
        self._min = 0
        self._max = 0

    def get_snap(self):
        if self._count == 0:
            return None
        return {"index":self._index,
                "count":self._count,
                "sum":self._sum,
                "avg":self._sum/self._count,
                "open":self._open,
                "close":self._close,
                "min":self._min,
                "max":self._max}

    def reduce(self, ticks, num, count=1):
        if ticks is None:
            return self.get_snap()

        if ticks <= self._last:
            return None

        index = int((ticks)/self._interval)
        if self._count == 0:
            self._index = index
            self._count = count
            self._last = ticks
            self._sum = count * num
            self._open = self._close = self._max = self._min = num
            return None
        elif index == self._index:
            self._index = index
            self._count += count
            self._last = ticks
            self._sum += count * num
            self._close = num
            self._max = max(self._max, num)
            self._min = min(self._min, num)
            return None
        else:
            t = self.get_snap()
            self._index = index
            self._count = count
            self._last = ticks
            self._sum = count * num
            self._open = self._close = self._max = self._min = num
            return t

    def expand(self, index):
        return self._interval * index
