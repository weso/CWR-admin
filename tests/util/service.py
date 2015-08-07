# -*- encoding: utf-8 -*-

import datetime

from cwr_admin.service.file import FileService
from cwr_admin.model.file import CWRFileData

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class TestFileService(FileService):
    def get_file(self, file_id):
        return CWRFileData(123, 'TEST', None, datetime.datetime.now(), 'ERROR', 'ERROR')

    def get_files(self):
        return [
            CWRFileData(123, 'TEST', None, datetime.datetime.now(), 'ERROR', 'ERROR')]

    def process_file(self, file):
        return 123

    def save_file(self, file):
        pass

    def delete_file(self, file):
        pass
