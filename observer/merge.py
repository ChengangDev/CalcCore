# -*- coding: utf-8 -*-

import numpy as np

class Merge:
    '''

    '''
    def __init__(self, interval, start=0):
        self._interval = interval
        self._start = start
        self._sum = 0
        self._count = 0
        self._index = 0
        self._last = 0

    def reduce(self, time, num, count=1):
        if time is None:
            return (self._index, self._sum)

        if time < self._last:
            return None

        index = int((time-self._start)/self._interval)
        if index == self._index or self._count == 0:
            self._last = time
            self._index = index
            self._sum += num * count
            self._count += count
            return None
        else:
            t = (self._index, self._sum)
            self._sum = num * count
            self._count = count
            self._last = time
            self._index = index
            return t

    def reduce_by_count(self, time, num, count=1):
        t_count = self._count
        t = self.reduce(time, num, count)
        if t is not None:
            return (t[0], t[1]/t_count)
        else:
            return None

    def reduce_by_interval(self, time, num):
        t = self.reduce(time, num)
        if t is not None:
            return (t[0], t[1]/self._interval)
        else:
            return None