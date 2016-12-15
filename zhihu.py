#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime

import const
import config
import exceptions


class Spider(object):

    session = None

    def __init__(self):
        self.session = requests.Session()

    def login(self):
        raise NotImplementedError()

    @property
    def date(self):
        return datetime.utcnow() \
            .strftime('%a, %d %b %Y %H:%M:%S GMT')

    def save_files(self, name, ret=None):
        pass


class ZhihuSpider(Spider):

    def __init__(self, user, password):
        assert user and password
        self.user = user
        self.password = password
        self.last_ret = None
        super(ZhihuSpider, self).__init__()

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

    def fetch(self, url, data=None, method='GET'):
        req = requests.Request(method, url)
        prepared = self.session.prepare_request(req)
        prepared.headers['Date'] = self.date
        prepared.headers['User-Agent'] = const.UA_CHROME
        ret = self.session.send(prepared)
        self.last_ret = ret
        return ret.text

    def save_files(self, name, ret=None):
        if ret is not None:
            ret = ret
        elif self.last_ret is not None:
            ret = self.last_ret
            self.last_ret = None
        else:
            raise exceptions.NoDownTaskError()
        with open(name, 'wb') as f:
            f.write(ret.content)


if __name__ == '__main__':
    zhihu = ZhihuSpider(
        config.ZHIHU_USER_PHONE,
        config.ZHIHU_USER_PASSWORD)
    zhihu.login('')
    html = zhihu.fetch(
        u'https://www.zhihu.com/topic/19559937/hot')
    zhihu.save_files('topic.html')
