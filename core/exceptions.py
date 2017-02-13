#!/usr/bin/env python
# coding: utf-8

import json


class BaseError(StandardError):

    error_code = 0
    error_desc = 'base error.'
    detail = 'an base error occured.'

    def __init__(
            self,
            error_code=None,
            error_desc=None,
            detail=None):
        super(BaseError, self).__init__()
        if error_code is not None:
            self.error_code = error_code
        if error_desc is not None:
            self.error_desc = error_desc
        if detail is not None:
            self.detail = detail

    def __str__(self):
        info = dict(
            error_code=self.error_code,
            error_desc=self.error_desc,
            detail=self.detail,
        )
        return json.dumps(info)

if __name__ == '__main__':
    try:
        raise BaseError
    except BaseError as e:
        print e
