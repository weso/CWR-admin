# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import datetime
import logging
import json
import threading

import requests
from werkzeug.utils import secure_filename
from cwr.parser.decoder.file import default_file_decoder
from requests.exceptions import ConnectionError
from cwr_admin.util.parallel import threaded

from cwr_admin.model.file import CWRFileData

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class FileService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_files(self):
        raise NotImplementedError('The get_files method must be implemented')

    @abstractmethod
    def get_file(self, id):
        raise NotImplementedError('The get_file method must be implemented')

    @abstractmethod
    def process_file(self, file):
        raise NotImplementedError('The process_file method must be implemented')

    @abstractmethod
    def save_file(self, file):
        raise NotImplementedError('The save_file method must be implemented')

    @abstractmethod
    def delete_file(self, file):
        raise NotImplementedError('The delete_file method must be implemented')


class FileProcessor(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process(self, data, file_id):
        raise NotImplementedError('The process method must be implemented')


class StatusChecker(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_status(self, file_id):
        raise NotImplementedError('The get_status method must be implemented')


class WSFileService(FileService):
    def __init__(self, url_cwr, service_id):
        super(FileService, self).__init__()
        self._files_data = {}
        self._decoder = default_file_decoder()

        self._url_cwr = url_cwr

        self._service_id = service_id

        self._logger = logging.getLogger(__name__)

    def get_file(self, file_id):
        self._logger.info('Acquiring file with id %s' % file_id)

        if file_id in self._files_data:
            data = self._files_data[file_id]
        else:
            data = None

        return data

    def get_files(self):
        self._logger.info('Acquiring all files')
        self._logger.info('Current list of threads: %s' % threading.enumerate())

        try:
            # files = requests.get(self._url_files).json()

            # files = json.loads(files)
            files = self._files_data.values()
        except (ConnectionError, ValueError):
            self._logger.info('Error requesting the files')
            files = []

        return files

    def save_file(self, file):
        self._files_data[file.file_id] = file
        matches = file.match

        if matches:
            matches = json.loads(matches)

            for match in matches:
                match['accepted'] = True

            self._files_data[file.file_id].match = json.dumps(matches)

    def delete_file(self, file_id):
        self._logger.info('Deleting file with id %s' % file_id)
        del self._files_data[file_id]

    def process_file(self, file):
        file_id = str(self._service_id.generate_id())
        file['file_id'] = file_id

        filename = secure_filename(file['filename'])

        self._files_data[file_id] = CWRFileData(file_id, filename, file,
                                                datetime.datetime.now(),
                                                'processing', 'none')

        self._send_file_to_process(file)

        return file_id

    @threaded
    def _send_file_to_process(self, file):
        headers = {'Content-Type': 'application/json'}

        try:
            requests.post(self._url_cwr, data=json.dumps(file), headers=headers)
        except (ConnectionError, ValueError):
            self._logger.info('Error sending the file')

    def reject_match(self, file_id, pos):
        file = self._files_data[file_id].match

        file = json.loads(file)

        file[pos - 1]['accepted'] = False
        file[pos - 1]['rejected'] = True

        # file.pop(pos - 1)

        self._files_data[file_id].match = json.dumps(file)

    def accept_match(self, file_id, pos):
        file = self._files_data[file_id].match

        file = json.loads(file)

        file[pos - 1]['accepted'] = True
        file[pos - 1]['rejected'] = False

        # file.pop(pos - 1)

        self._files_data[file_id].match = json.dumps(file)
