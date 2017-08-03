# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
from datetime import timedelta
import multiprocessing
import time

from operate import observe

class ObProcess(multiprocessing.Process):
    def __init__(self, code, simulate=False):
        multiprocessing.Process.__init__(self)
        self._code = code
        self._simulate = simulate
        self._ob = observe.CliffObserver(code)

    def run(self):
        print("Start process {0}".format(self._code))
        if self._simulate is False:
            self._ob.start()
        else:
            self._ob.simulate(date='2017-06-15', fetch_interval=0)

        print("Exit process {0}".format(self.name))


if __name__ == "__main__":
    codes = ['600004', '002415', '000776', '600988', '601318', '601555', '600895', '600398']
    #codes = ['002415']
    procs = []
    for code in codes:
        p = ObProcess(code, False)
        p.start()
        procs.append(p)
        time.sleep(2)

    for p in procs:
        p.join()

    print("Exits main")