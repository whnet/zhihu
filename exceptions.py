#!/usr/bin/env python
# coding: utf-8

import json


class SpiderException(Exception):
    '''Base class of exceptions reference by this project.'''
    code = 1000
    error = 'spider error.'
    detail = u'爬虫异常'

    def _repr__(self):
        error = dict(
            code=self.code,
            error=self.error,
            detail=self.detail)
        return json.dumps(error)


class LoginError(SpiderException):

    code = 1001
    error = 'login error.'
    detail = u'登录失败'


class NoDownTaskError(SpiderException):

    code = 1002
    error = 'no download task find.'
    detail = u'未找到下载文件'
