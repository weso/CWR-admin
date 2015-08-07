# -*- encoding: utf-8 -*-

"""
Web app module.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from logging import Formatter

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.restful import Api

from cwr_admin.config import DevConfig
from data_admin.accessor import CWRValidatorConfiguration
from cwr_admin.resources import CWRProcessorResource, CWRFilesResource, \
    CWRMatchResultResource, CWRFilesRemoveResource, CWRMatchBeginResource, \
    CWRMatchRejectResource, CWRMatchAcceptResource, CWRMatchFeedbackResource
from cwr_admin.service import WSFileService, UUIDIdentifierService, \
    WSMatchingService

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


def _register_resources(api):
    api.add_resource(CWRProcessorResource, '/cwr/process/')
    api.add_resource(CWRFilesResource, '/cwr/files/')
    api.add_resource(CWRFilesRemoveResource, '/cwr/files/remove/')
    api.add_resource(CWRMatchResultResource, '/cwr/match/')
    api.add_resource(CWRMatchBeginResource, '/cwr/match/begin/')
    api.add_resource(CWRMatchRejectResource, '/cwr/match/reject/')
    api.add_resource(CWRMatchAcceptResource, '/cwr/match/confirm/')
    api.add_resource(CWRMatchFeedbackResource, '/cwr/match/feedback/')


def _load_services(app):
    match_ws = os.environ.get('CWR_MATCH_WS',
                              'http://127.0.0.1:33567/cwr/')
    file_ws = os.environ.get('CWR_FILE_WS',
                             'http://127.0.0.1:33568/')

    app.config['ID_SERVICE'] = UUIDIdentifierService()
    app.config['MATCH_SERVICE'] = \
        WSMatchingService(match_ws + 'file/',
                          match_ws + 'results/',
                          match_ws + 'feedback/')
    app.config['FILE_SERVICE'] = WSFileService(file_ws + 'upload/',
                                               app.config['ID_SERVICE'])


def create_app(config_object=DevConfig):
    config = CWRValidatorConfiguration().get_config()

    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_object)

    _register_resources(api)
    _load_services(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    if app.config['DEBUG']:
        log = config['log.folder']
        if len(log) == 0:
            log = 'cwr_store_ws.log'

        handler = RotatingFileHandler(log, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            Formatter('[%(levelname)s][%(asctime)s] %(message)s'))

        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('').addHandler(handler)

        app.logger.addHandler(handler)

    return app
