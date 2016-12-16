#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, date


def model_to_dict(model):
    ret = dict()
    for attr in dir(model):
        if attr.starts_with('-'):
            continue
        o = getattr(model, attr)
        if isinstance(o, (datetime, date)):
            ret[attr] = o.isoformat()
        ret[attr] = o
    ret.pop('metadata', None)
    return ret


if __name__ == '__main__':
    pass
