# -*- encoding: utf-8 -*-

import unittest

from cwr_admin.service import WSFileService, UUIDIdentifierService

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class _Object(object):
    pass


class TestWSFileServiceInvalidConnection(unittest.TestCase):
    def setUp(self):
        self._service = WSFileService('http://localhost:1',
                                      UUIDIdentifierService())

    def test_get_file(self):
        file_data = self._service.get_file(123)

        self.assertEqual(file_data, None)

    def test_get_files(self):
        files = self._service.get_files()

        self.assertEqual(len(files), 0)

    def test_process_file(self):
        file = {
            'filename': 'filename',
            'contents': 'contents',
        }

        self._service.process_file(file)


class TestWSFileServiceNoWS(unittest.TestCase):
    def setUp(self):
        self._service = WSFileService('http://somewhere.com',
                                      UUIDIdentifierService())

    def test_get_file(self):
        file_data = self._service.get_file(123)

        self.assertEqual(file_data, None)

    def test_get_files(self):
        files = self._service.get_files()

        self.assertEqual(len(files), 0)

    def test_process_file(self):
        file_data = {
            'filename': 'filename',
            'contents': 'contents',
        }

        self._service.process_file(file_data)
