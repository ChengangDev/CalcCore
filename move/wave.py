# -*- coding: utf-8 -*-

import numpy as np

class WElem(object):
    ''''''
    __slots__ = ('_t', '_v', '_diff')
    def __init__(self, t, v):
        self._t = t
        self._v = v


class Wave:
    '''

    '''
    def __init__(self):
        self._count = 0
        self._peaks = []


    def push(self, t, num):
        elem = WElem(t, num)
        self._count += 1
        if len(self._peaks) == 0:
            self._peaks.append(elem)
        elif len(self._peaks) == 1:
            if self._peaks[0].v != elem._v:
                self._peaks.append(elem)
        else:
            cur = len(self._peaks) - 1
            if self._peaks[cur]._v < self._peaks[cur-1]._v:
                if self._peaks[cur]._v > elem._v:
                    self._peaks[cur] = elem
                elif self._peaks[cur]._v < elem._v:
                    self._peaks.append(elem)
            elif self._peaks[cur]._v > self._peaks[cur-1]._v:
                if self._peaks[cur]._v < elem._v:
                    self._peaks[cur] = elem
                elif self._peaks[cur]._v > elem._v:
                    self._peaks.append(elem)


class PostSwing:
    '''

    '''
    def __init__(self, max_size=240):
        self._count = 0
        self._max_size = max_size
        self._q = [0.0 for x in range(max_size)]
        self._post_min = [0.0 for x in range(max_size)]
        self._post_max = [0.0 for x in range(max_size)]
        self._post_swing = [0.0 for x in range(max_size)]

    def push(self, num):
        if self._count >= self._max_size:
            return

        idx = self._count
        self._post_max[idx] = self._post_min[idx] = self._q[idx] = num
        for idx in range(self._count):
            self._post_min[idx] = min(self._post_min[idx], num)
            self._post_max[idx] = max(self._post_max[idx], num)

        self._count += 1

    def pop(self):
        if self._count == 0:
            return


class PrevSwing:
    '''

    '''
    def __init__(self, max_size=240):
        self._count = 0
        self._max_size = max_size
        self._q = [0.0 for x in range(max_size)]
        self._prev_min = [0.0 for x in range(max_size)]
        self._prev_max = [0.0 for x in range(max_size)]
        self._prev_swing = [0.0 for x in range(max_size)]

    def push(self, num):
        if self._count >= self._max_size:
            return

        idx = self._count
        self._q[idx] = num
        if idx == 0:
            self._prev_max[idx] = self._prev_min[idx] = num
        else:
            self._prev_min[idx] = min(self._prev_min[idx-1], num)
            self._prev_max[idx] = max(self._prev_max[idx-1], num)

        self._count += 1

    def pop(self):
        if self._count == 0:
            return

        self._count -= 1

