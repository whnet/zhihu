#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime

import const
import config
import exceptions


class ZhihuSpider(object):

    session = None

    def __init__(self, user, password):
        assert user and password
        self.session = requests.Session()
        self.user = user
        self.password = password
        super(ZhihuSpider, self).__init__()

    @property
    def date(self):
        return datetime.utcnow() \
            .strftime('%a, %d %b %Y %H:%M:%S GMT')

    def login(self, catpcha):
        data = {
            'phone_num': self.user,
            'password': self.password,
        }
        req = requests.Request(
            'POST',
            'https://www.zhihu.com/login/phone_num',
            data=data,
        )
        prepared = self.session.prepare_request(req)
        prepared.headers['Date'] = self.date
        prepared.headers['User-Agent'] = const.UA_CHROME
        ret = self.session.send(prepared)
        if ret.status_code != 200:
            raise exceptions.LoginError()

    def fetch(self, url, data=None,
              headers=None, method='GET'):
        req = requests.Request(
            method, url, data=data,
            headers=headers)
        prepared = self.session.prepare_request(req)
        prepared.headers['Date'] = self.date
        prepared.headers['User-Agent'] = const.UA_CHROME
        ret = self.session.send(prepared)
        return ret


if __name__ == '__main__':
    zhihu = ZhihuSpider(
        config.ZHIHU_USER_PHONE,
        config.ZHIHU_USER_PASSWORD)
    zhihu.login('')
    html = zhihu.fetch(
        u'https://www.zhihu.com/topic/19559937/top-answers?page=3')
