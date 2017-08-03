# -*- coding: utf-8 -*-

import numpy as np

class Trend:
    '''

    '''
    def __init__(self, max_size=240):
        self._count = 0
        self._max_size = max_size
        self._q = [ 0.0 for x in range(max_size) ]
        self._inc_max_len = np.zeros(shape=(max_size, max_size), dtype=float)
        self._dec_max_len = np.zeros(shape=(max_size, max_size), dtype=float)

    def push(self, num):
        if self._count >= self._max_size:
            return

    def _lis(self, i):
        if i >= self._max_size:
            return

    def _lds(self, i):
        if i >= self._max_size:
            return