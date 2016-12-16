#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import requests

import const


class Spider(object):

    session = None

    def __init__(self, user, password):
        self.session = requests.Session()
        self.user = user
        self.password = password
        super(Spider, self).__init__()

    def fetch(self, url, method='GET', **options):
        req = requests.Request(
            method, url,
            data=options.get('data'),
            headers=options.get('headers'))
        prepared = self.session.prepare_request(req)
        prepared.headers['Date'] = self.date
        prepared.headers['User-Agent'] = const.UA_CHROME
        ret = self.session.send(prepared)
        return ret.text

    def login(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    def date(self):
        return datetime.utcnow() \
            .strftime('%a, %d %b %Y %H:%M:%S GMT')
