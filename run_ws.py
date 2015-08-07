# -*- encoding: utf-8 -*-
import os

from cwr_admin import create_app

"""
Runs the CWR Validator web API.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__version__ = '0.0.0'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33508))
    host = os.environ.get('HOST', '127.0.0.1')

    app = create_app()

    app.run(host=host, port=port)
