# -*- encoding: utf-8 -*-
import logging
import datetime
import json

from flask.ext.restful import marshal
from flask import current_app
from flask_restful import Resource, reqparse

from cwr_admin.model.file import CWRFileData, cwr_file_fields, cwr_file_fields_small

"""
Flask RESTful resources for the file uploading endpoints.

These take handle of receiving and processing files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

_logger = logging.getLogger(__name__)


class CWRProcessorResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def __init__(self):
        super(CWRProcessorResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('filename', type=unicode, required=True,
                                    help='No file name provided',
                                    location='json')
        self._reqparse.add_argument('contents', type=unicode, required=True,
                                    help='No file name provided',
                                    location='json')

    def get(self):
        """
        Getting from the uploads endpoint is disallowed.

        A message is returned to indicate this.

        :return: a message warning that the get command is disallowed
        """
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        """
        Posts a file to the endpoint.

        It should receive a file, which can have any name, as it will just take the first file on the request.

        :return:
        """
        _logger.info('Received CWR file')

        cwr_data = self._reqparse.parse_args()

        _logger.info('Accepted CWR file %s' % cwr_data['filename'])

        file_service = current_app.config['FILE_SERVICE']

        file_id = file_service.process_file(cwr_data)

        file = CWRFileData(file_id, cwr_data['filename'], None,
                           datetime.datetime.now(), 'processing', 'none')

        file_service.save_file(file)

        return '', 200


class CWRFilesResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def __init__(self):
        super(CWRFilesResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('data', type=unicode, required=False,
                                    help='No file data provided',
                                    location='json')
        self._reqparse.add_argument('id', type=str, required=True,
                                    help='No file id provided',
                                    location='json')

        self._fileparse = reqparse.RequestParser()
        self._fileparse.add_argument('id', type=str, location='json')

    def get(self):
        _logger.info('Asked for CWR files')
        file_service = current_app.config['FILE_SERVICE']

        file_data = self._fileparse.parse_args()

        if 'id' in file_data and file_data['id']:
            _logger.info('Asked for file with id %s' % file_data['id'])
            result = file_service.get_file(file_data['id'])

            result = marshal(result, cwr_file_fields)
        else:
            _logger.info('Asked for all CWR files')
            files = file_service.get_files()

            result = []
            for file in files:
                result.append(marshal(file, cwr_file_fields_small))

        return result

    def post(self):
        """
        Posts a file to the endpoint.

        It should receive a file, which can have any name, as it will just take the first file on the request.

        :return:
        """
        _logger.info('Received processed CWR file')

        cwr_data = self._reqparse.parse_args()

        _logger.info('Accepted processed CWR file')

        file_service = current_app.config['FILE_SERVICE']

        file_id = cwr_data['id']
        file = file_service.get_file(file_id)

        if file:
            if cwr_data['data']:
                file.contents = cwr_data['data']

                file_service = current_app.config['FILE_SERVICE']

                file = file_service.get_file(file_id)

                file.parse_status = 'done'
            else:
                file.parse_status = 'error'

            return '', 200
        else:
            return '', 404


class CWRFilesRemoveResource(Resource):
    def __init__(self):
        super(CWRFilesRemoveResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=str, required=True,
                                    help='No file id provided',
                                    location='json')

    def post(self):
        _logger.info('Asked to remove CWR file')

        file_id = self._reqparse.parse_args()['file_id']

        _logger.info('Removing file %s' % file_id)

        file_service = current_app.config['FILE_SERVICE']

        file_service.delete_file(file_id)


class CWRMatchRejectResource(Resource):
    def __init__(self):
        super(CWRMatchRejectResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=str, required=True,
                                    help='No file id provided',
                                    location='json')
        self._reqparse.add_argument('pos', type=int, required=True,
                                    help='No match # provided',
                                    location='json')

    def post(self):
        _logger.info('Asked to remove CWR file')

        args = self._reqparse.parse_args()

        file_id = args['file_id']
        pos = args['pos']

        _logger.info('Rejecting match for file %s' % file_id)

        file_service = current_app.config['FILE_SERVICE']

        file_service.reject_match(file_id, pos)


class CWRMatchAcceptResource(Resource):
    def __init__(self):
        super(CWRMatchAcceptResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=str, required=True,
                                    help='No file id provided',
                                    location='json')
        self._reqparse.add_argument('pos', type=int, required=True,
                                    help='No match # provided',
                                    location='json')

    def post(self):
        _logger.info('Asked to accept match')

        args = self._reqparse.parse_args()

        file_id = args['file_id']
        pos = args['pos']

        _logger.info('Accepting match for file %s' % file_id)

        file_service = current_app.config['FILE_SERVICE']

        file_service.accept_match(file_id, pos)


class CWRMatchBeginResource(Resource):
    def __init__(self):
        super(CWRMatchBeginResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=unicode, required=True,
                                    help='No file ID provided',
                                    location='json')

    def get(self):
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        _logger.info('Asked to begin matching')

        args = self._reqparse.parse_args()

        file_id = args['file_id']

        file_service = current_app.config['FILE_SERVICE']

        file = file_service.get_file(file_id)

        match_service = current_app.config['MATCH_SERVICE']

        match_service.match(file.contents, file_id)

        file.match_status = 'processing'

        return '', 200


class CWRMatchResultResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def __init__(self):
        super(CWRMatchResultResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=unicode, required=True,
                                    help='No file ID provided',
                                    location='json')
        self._reqparse.add_argument('match', type=list, required=True,
                                    help='No match results provided',
                                    location='json')

    def get(self):
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        _logger.info('Received match results')

        match_results = self._reqparse.parse_args()

        _logger.info('Accepted match results')

        file_service = current_app.config['FILE_SERVICE']

        file = file_service.get_file(match_results['file_id'])

        file.match = json.dumps(match_results['match'])
        file.match_status = 'done'

        matches = file.match

        matches = json.loads(matches)

        for match in matches:
            match['accepted'] = True

        file.match = json.dumps(matches)

        return '', 200


class CWRMatchFeedbackResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def __init__(self):
        super(CWRMatchFeedbackResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=unicode, required=True,
                                    help='No file ID provided',
                                    location='json')

    def get(self):
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        _logger.info('Received match feedback petition')

        file_id = self._reqparse.parse_args()['file_id']

        _logger.info('Accepted match results')

        file_service = current_app.config['FILE_SERVICE']
        match_service = current_app.config['MATCH_SERVICE']

        file = file_service.get_file(file_id)

        match_service.match_feedback(file.match, file.name, file_id)

        return '', 200
