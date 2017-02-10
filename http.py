#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime

import gevent
import requests
from gevent import monkey
monkey.patch_all()  # noqa

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
      'Safari/537.36')


class HttpClient(object):

    def __init__(self, tries=5):
        self.session = requests.Session()
        self.tries = tries

    def fetch(self, url, method='GET', data=None, **options):
        req = requests.Request(
            method,
            url,
            data=data,
            headers=options.get('headers'),
            cookies=options.get('cookies'))
        req = self.session.prepare_request(req)
        req.headers['Date'] = datetime.now().strftime(
            '%a, %d %b %Y %H:%M:%S GMT')
        req.headers['User-Agent'] = UA
        for i in range(self.tries):
            try:
                resp = self.session.send(req)
            except:
                gevent.sleep(0.5)
                continue
            if resp:
                break
        else:
            raise StandardError(u'网络请求失败.')
        return resp
