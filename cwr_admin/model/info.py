# -*- encoding: utf-8 -*-

"""
Offers services for CWR files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class CompanyInfo(object):
    def __init__(self, name, url):
        self._name = name
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url


class ApplicationInfo(object):
    def __init__(self, name, year, cms_url, cms_name):
        self._name = name
        self._year = year
        self._cms_url = cms_url
        self._cms_name = cms_name

    @property
    def name(self):
        return self._name

    @property
    def year(self):
        return self._year

    @property
    def cms_name(self):
        return self._cms_name

    @property
    def cms_url(self):
        return self._cms_url
