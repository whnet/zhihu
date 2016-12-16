#!/usr/bin/env python
# coding: utf-8

from contextlib import closing
from datetime import datetime
import requests

import const
from db import Session
from model import Proxy
from tools import model_to_dict


class Spider(object):

    session = None
    proxies = []

    def __init__(self, user, password):
        self.session = requests.Session()
        self.user = user
        self.password = password
        super(Spider, self).__init__()

    def init_proxies(self):
        with closing(Session()) as session:
            proxies = []
            for _proxy in session.query(Proxy) \
                    .filter(Proxy.deleted == 0) \
                    .order_by(Proxy.score.desc()) \
                    .all():
                proxies.append(model_to_dict(_proxy))
            self.proxies = proxies

    def fetch(self, url, method='GET', **options):
        req = requests.Request(
            method, url,
            data=options.get('data'),
            headers=options.get('headers'),
            cookies=options.get('cookies'))
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
