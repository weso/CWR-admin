# -*- encoding: utf-8 -*-

"""
Offers services for CWR files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class WorkloadInfo(object):
    def __init__(self, number, file, status):
        self._number = number
        self._file = file
        self._status = status

    @property
    def file(self):
        return self._file

    @property
    def number(self):
        return self._number

    @property
    def status(self):
        return self._status
