# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import date

class Quant:
    ''''''
    def __init__(self, start, time_format='%H:%M:%S'):
        self._start = start
        self._time_format = time_format
        self._start_object = datetime.strptime(start, time_format)

    def time_to_seconds(self, time):
        time_object = datetime.strptime(time, self._time_format)
        return (time_object.hour-self._start_object.hour) * 3600 + (time_object.minute-self._start_object.minute)*60 + time_object.second - self._start_object.second

    def seconds_to_time(self, seconds):
        time_object = self._start_object + timedelta(seconds=seconds)
        return datetime.strftime(time_object, self._time_format)


class QuantCN(Quant):

    def __init__(self):
        Quant.__init__(self, '9:30:00', '%H:%M:%S')
        self._noon_end = Quant.time_to_seconds(self, '13:00:00')
        self._noon_start = Quant.time_to_seconds(self, '11:30:00')
        self._noon_offset = self._noon_end - self._noon_start

    @staticmethod
    def today():
        return date.today().isoformat()

    def time_to_seconds(self, time):
        seconds = Quant.time_to_seconds(self, time)
        if seconds < self._noon_end:
            return seconds
        else:
            return seconds - self._noon_offset

    def seconds_to_time(self, seconds):
        if seconds > self._noon_start:
            seconds += self._noon_offset
        return Quant.seconds_to_time(self, seconds)