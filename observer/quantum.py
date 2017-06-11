# -*- coding: utf-8 -*-

from datetime import datetime

class CN:
    ''''''
    def __init__(self, start, time_format='%H:%M:%S'):
        self._start = start
        self._time_format = time_format
        self._start_object = datetime.strptime(start, time_format)

    def get_seconds(self, time):
        time_object = datetime.strptime(time, self._time_format)
        return (time_object.hour-self._start_object.hour) * 3600 + (time_object.minute-self._start_object.minute)*60 + time_object.second - self._start_object.second

