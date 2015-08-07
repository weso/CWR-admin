# -*- encoding: utf-8 -*-

from flask.ext.restful import fields

"""
Offers services for CWR files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

cwr_file_fields = {
    'file_id': fields.String,
    'name': fields.String,
    'contents': fields.String,
    'date': fields.DateTime,
    'parse_status': fields.String,
    'match_status': fields.String,
    'match': fields.String
}
cwr_file_fields_small = {
    'file_id': fields.String,
    'name': fields.String,
    'date': fields.DateTime,
    'parse_status': fields.String,
    'match_status': fields.String,
}


class CWRFileData(object):
    def __init__(self, file_id, name, contents, date, parse_status,
                 match_status):
        self._file_id = file_id
        self._name = name
        self._contents = contents
        self._date = date
        self._match_status = match_status
        self._parse_status = parse_status
        self._match = None

    @property
    def contents(self):
        return self._contents

    @property
    def date(self):
        return self._date

    @property
    def file_id(self):
        return self._file_id

    @property
    def parse_status(self):
        return self._parse_status

    @property
    def name(self):
        return self._name

    @property
    def match(self):
        return self._match

    @property
    def match_status(self):
        return self._match_status

    @contents.setter
    def contents(self, contents):
        self._contents = contents

    @date.setter
    def date(self, date):
        self._date = date

    @file_id.setter
    def file_id(self, file_id):
        self._file_id = file_id

    @parse_status.setter
    def parse_status(self, parse_status):
        self._parse_status = parse_status

    @name.setter
    def name(self, name):
        self._name = name

    @match.setter
    def match(self, match):
        self._match = match

    @match_status.setter
    def match_status(self, match_status):
        self._match_status = match_status
