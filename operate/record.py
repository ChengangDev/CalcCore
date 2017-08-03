# -*- coding: utf-8 -*-
import logging

class Note(object):
    ''''''

    def __init__(self):
        self._lg = logging.getLogger('')

    def info(self, msg):
        self._lg.info(msg)

    def debug(self, msg):
        self._lg.debug(msg)

    def warning(self, msg):
        self._lg.warning(msg)
