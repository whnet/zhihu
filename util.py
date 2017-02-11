#!/usr/bin/env python
# coding: utf-8

import os
import fcntl
from functools import wraps


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


if __name__ == '__main__':
    pass
