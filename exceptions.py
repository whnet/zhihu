#!/usr/bin/env python
# coding: utf-8

import json


class SpiderException(Exception):

    code = 1000
    error = 'spider error.'
    detail = u'爬虫异常'

    def __init__(self, message=None):
        if message is not None:
            self.detail = message

    def __str__(self):
        error = dict(
            code=self.code,
            error=self.error,
            detail=self.detail)
        return json.dumps(error)


class LoginError(SpiderException):

    code = 1001
    error = 'login error.'
    detail = u'登录失败'


if __name__ == '__main__':
    try:
        raise SpiderException()
    except Exception as e:
        print e
