# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import json
import logging

import requests

"""
Offers services for CWR files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class MatchingService(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def match(self, cwr_json, file_id):
        raise NotImplementedError('The match method must be implemented')

    @abstractmethod
    def get_match_result(self, file_id):
        raise NotImplementedError(
            'The get_match_result method must be implemented')


class TestMatchingService(object):
    def __init__(self):
        super(TestMatchingService, self).__init__()

        json_data = '[ { "query" : "Shakira I. Mebarack", "type_of_query" : "artist", "refinements" : [ { "type": "song", "content" : "Waka Waka" }, { "type" : "song", "content" : "La Tortura" } ], "results" : [ { "entity" : "http://example.org/Shakira", "raw_score" : 0.95, "matched_forms" : { "Shakira Isabel Mebarack" : 0.75, "Shakira Mebarack" : 0.95 }, "refined_score" : 2.95, "refinements": [ { "type" : "song", "score" : 1, "relevance" : 1, "content" : "Waka Waka", "matched_forms" : { "Waka_Waka" : 1, "Waka Waka feat" : 0.85 } }, { "type" : "song", "score" : 1, "relevance" : 1, "content" : "La Tortura", "matched_forms" : { "La Tortura" : 1 } } ] }, { "entity" : "http://example.org/Schakira", "raw_score" : 0.4, "matched_forms" : { "Schakira" : 0.4 }, "refined_score" : 0.4, "refinements": [] } ] } ]'

        self._json = json.loads(json_data)

    def match(self, cwr_json, file_id):
        pass

    def get_match_result(self, file_id):
        return self._json


class WSMatchingService(object):
    def __init__(self, url_match, url_results, url_feedback):
        super(WSMatchingService, self).__init__()
        self._url_match = url_match
        self._url_results = url_results
        self._url_feedback = url_feedback

        self._logger = logging.getLogger(__name__)

    def match_feedback(self, cwr_json, filename, file_id):
        self._logger.info("Sending feedback for file with id %s" % file_id)

        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        cwr_match = {'file_id': file_id, 'cwr': cwr_json, 'filename': filename}

        cwr_match = json.dumps(cwr_match)

        try:
            # TODO: Don't catch the error like this. Handle each error case.
            requests.post(self._url_feedback, data=cwr_match, headers=headers,
                          verify=False)
        except:
            self._logger.error(
                "Error sending file with id %s for matching" % file_id)

    def match(self, cwr_json, file_id, config=None):
        self._logger.info("Matching file with id %s" % file_id)

        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        self._logger.info("Posting file's data to %s" % self._url_match)

        cwr_match = {'file_id': file_id, 'cwr': json.loads(cwr_json)}
        if config:
            cwr_match['config'] = config

        cwr_match = json.dumps(cwr_match)

        try:
            # TODO: Don't catch the error like this. Handle each error case.
            requests.post(self._url_match, data=cwr_match, headers=headers,
                          verify=False)
        except:
            self._logger.error(
                "Error sending file with id %s for matching" % file_id)

    def get_match_result(self, file_id):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        data = {}
        data['file_id'] = file_id
        data = json.dumps(data)

        try:
            # TODO: Don't catch the error like this. Handle each error case.
            json_data = requests.get(self._url_results, data=data,
                                     headers=headers).json()
            result = json.loads(json_data['results'])
        except:
            result = None

        return result
