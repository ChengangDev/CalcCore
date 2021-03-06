# -*- coding: utf-8 -*-

import numpy as np
from collections import Sequence


class RingBuffer(Sequence):
    def __init__(self, capacity, dtype=float, allow_overwrite=True):
        """
		Create a new ring buffer with the given capacity and element type

		Parameters
		----------
		capacity: int
			The maximum capacity of the ring buffer
		dtype: data-type, optional
			Desired type of buffer elements. Use a type like (float, 2) to
			produce a buffer with shape (N, 2)
		allow_overwrite: bool
			If false, throw an IndexError when trying to append to an alread
			full buffer
		"""
        self._arr = np.zeros(capacity, dtype)
        self._left_index = 0
        self._right_index = 0
        self._capacity = capacity
        self._allow_overwrite = allow_overwrite

    def _unwrap(self):
        """ Copy the data from this buffer into unwrapped form """
        return np.concatenate((
            self._arr[self._left_index:min(self._right_index, self._capacity)],
            self._arr[:max(self._right_index - self._capacity, 0)]
        ))

    def _fix_indices(self):
        """
		Enforce our invariant that 0 <= self._left_index < self._capacity
		"""
        if self._left_index >= self._capacity:
            self._left_index -= self._capacity
            self._right_index -= self._capacity
        elif self._left_index < 0:
            self._left_index += self._capacity
            self._right_index += self._capacity

    @property
    def is_full(self):
        """ True if there is no more space in the buffer """
        return len(self) == self._capacity

    # numpy compatibility
    def __array__(self):
        return self._unwrap()

    @property
    def dtype(self):
        return self._arr.dtype

    @property
    def shape(self):
        return (len(self),) + self._arr.shape[1:]

    # these mirror methods from deque
    @property
    def maxlen(self):
        return self._capacity

    def append(self, value):
        if self.is_full:
            if not self._allow_overwrite:
                raise IndexError('append to a full RingBuffer with overwrite disabled')
            elif not len(self):
                return
            else:
                self._left_index += 1

        self._arr[self._right_index % self._capacity] = value
        self._right_index += 1
        self._fix_indices()

    def push(self, value):
        if self.is_full:
            if not self._allow_overwrite:
                raise IndexError('append to a full RingBuffer with overwrite disabled')
            elif not len(self):
                return
            else:
                self._right_index -= 1

        self._left_index -= 1
        self._fix_indices()
        self._arr[self._left_index] = value

    def pop(self):
        if len(self) == 0:
            raise IndexError("pop from an empty RingBuffer")
        self._right_index -= 1
        self._fix_indices()
        res = self._arr[self._right_index % self._capacity]
        return res

    def popleft(self):
        if len(self) == 0:
            raise IndexError("pop from an empty RingBuffer")
        res = self._arr[self._left_index]
        self._left_index += 1
        self._fix_indices()
        return res

    def extend(self, values):
        lv = len(values)
        if len(self) + lv > self._capacity:
            if not self._allow_overwrite:
                raise IndexError('extend a RingBuffer such that it would overflow, with overwrite disabled')
            elif not len(self):
                return
        if lv >= self._capacity:
            # wipe the entire array! - this may not be threadsafe
            self._arr[...] = values[-self._capacity:]
            self._right_index = self._capacity
            self._left_index = 0
            return

        ri = self._right_index % self._capacity
        sl1 = np.s_[ri:min(ri + lv, self._capacity)]
        sl2 = np.s_[:max(ri + lv - self._capacity, 0)]
        self._arr[sl1] = values[:sl1.stop - sl1.start]
        self._arr[sl2] = values[sl1.stop - sl1.start:]
        self._right_index += lv

        self._left_index = max(self._left_index, self._right_index - self._capacity)
        self._fix_indices()

    def extendleft(self, values):
        lv = len(values)
        if len(self) + lv > self._capacity:
            if not self._allow_overwrite:
                raise IndexError('extend a RingBuffer such that it would overflow, with overwrite disabled')
            elif not len(self):
                return
        if lv >= self._capacity:
            # wipe the entire array! - this may not be threadsafe
            self._arr[...] = values[:self._capacity]
            self._right_index = self._capacity
            self._left_index = 0
            return

        self._left_index -= lv
        self._fix_indices()
        li = self._left_index
        sl1 = np.s_[li:min(li + lv, self._capacity)]
        sl2 = np.s_[:max(li + lv - self._capacity, 0)]
        self._arr[sl1] = values[:sl1.stop - sl1.start]
        self._arr[sl2] = values[sl1.stop - sl1.start:]

        self._right_index = min(self._right_index, self._left_index + self._capacity)

    # implement Sequence methods
    def __len__(self):
        return self._right_index - self._left_index

    def __getitem__(self, index):
        # handle simple (b[1]) and basic (b[np.array([1, 2, 3])]) fancy indexing specially
        if not isinstance(index, tuple):
            index_arr = np.asarray(index)
            if issubclass(index_arr.dtype.type, np.integer):
                index_arr = (index_arr + self._left_index) % self._capacity
                return self._arr[index_arr]

        # for everything else, get it right at the expense of efficiency
        return self._unwrap()[index]

    def __setitem__(self, index, item):
        index = (index + self._left_index) % self._capacity
        self._arr[index] = item


    def __iter__(self):
        # alarmingly, this is comparable in speed to using itertools.chain
        return iter(self._unwrap())

    # Everything else
    def __repr__(self):
        return '<RingBuffer of {!r}>'.format(np.asarray(self))


class Move:
    '''
    '''

    def __init__(self, calc_size=60):
        self._calc_size = calc_size
        self._q = RingBuffer(calc_size, float)
        self._mvavg = [0.0 for x in range(calc_size)]
        self._mvsum = [0.0 for x in range(calc_size)]
        self._mvmin = [0.0 for x in range(calc_size)]
        self._mvmax = [0.0 for x in range(calc_size)]
        self._count = 0

    def push(self, num):
        self._q.push(num)
        self._count += 1
        self.__mvall()

    def pop(self):
        self._q.pop()
        self._count -= 1
        self.__mvall()

    def t_minus(self, n):
        return self._q[n]

    def ma(self, n):
        return self._mvavg[n-1]

    def msum(self, n):
        return self._mvsum[n-1]

    def mmax(self, n):
        return self._mvmax[n-1]

    def mmin(self, n):
        return self._mvmin[n-1]

    def __mvall(self):
        self._mvmin[0] = self._q[0]
        self._mvmax[0] = self._q[0]
        self._mvsum[0] = self._q[0]
        self._mvavg[0] = self._q[0]

        for i in range(1, self._calc_size):
            if i >= self._count:
                self._mvmin[i] = self._mvmin[i-1]
                self._mvmax[i] = self._mvmax[i-1]
                self._mvsum[i] = self._mvsum[i-1]
                self._mvavg[i] = self._mvavg[i-1]
            else:
                self._mvmin[i] = min(self._mvmin[i-1], self._q[i])  #wrong
                self._mvmax[i] = max(self._mvmax[i-1], self._q[i])
                self._mvsum[i] = (self._mvsum[i-1] + self._q[i])
                self._mvavg[i] = float(self._mvsum[i] / (i+1))


class RMove(Move):
    '''

    '''
    def __init__(self, pivot, calc_size=60):
        self._pivot = pivot
        Move.__init__(self, calc_size)

    def push(self, num):
        Move.push(self, (num-self._pivot)/self._pivot)


class DRMove(Move):
    '''

    '''
    def __init__(self, pivot, calc_size=60):
        self._pivot = pivot
        self._last = pivot
        Move.__init__(self, calc_size)

    def push(self, num):
        Move.push(self, (num-self._last)/self._pivot)
        self._last = num


class MMove(Move):
    '''

    '''
    def __init__(self, open, calc_size=4800):
        self._open = open
        self._last = open
        Move.__init__(self, calc_size)

    def push(self, price, count, duration):
        Move.push(abs(price-self._last)/(price*count)*duration)
        self._last = price