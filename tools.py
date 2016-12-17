#!/usr/bin/env python
# coding: utf-8

import os
import fcntl
from fuctools import wraps
from datetime import datetime, date


def singleton(pid_filename):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            pid = str(os.getpid())
            pidfile = open(pid_filename, 'a+')
            try:
                fcntl.flock(pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                return
            pidfile.seek(0)
            pidfile.truncate()
            pidfile.write(pid)
            pidfile.flush()
            pidfile.seek(0)

            ret = f(*args, **kwargs)

            try:
                pidfile.close()
            except IOError as err:
                if err.errno != 9:
                    return
            os.remove(pid_filename)
            return ret
        return decorated
    return decorator


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
