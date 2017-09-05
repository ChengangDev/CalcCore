# -*- coding: utf-8 -*-
import logging

class Note(object):
    ''''''

    def __init__(self, name=''):
        self._lg = logging.getLogger(name)


    def info(self, msg):
        self._lg.info(msg)

    def debug(self, msg):
        self._lg.debug(msg)

    def warning(self, msg):
        self._lg.warning(msg)

    def error(self, msg):
        self._lg.error(msg)

    def critical(self, msg):
        self._lg.critical(msg)

class NoteCliff(Note):

    def __init__(self):

        Note.__init__(log)

