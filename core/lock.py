#!/usr/bin/env python
# coding: utf-8

from __future__ import with_statement

import contextlib
from abc import ABCMeta, abstractmethod

from db import Session


class Lock(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def lock(self):
        raise NotImplementedError

    @abstractmethod
    def unlock(self):
        raise NotImplementedError


class DBLock(Lock):

    def lock(self):
        with contextlib.closing(Session()) as session:
            sql = (
                "select *from crawler_value where "
                "name = 'crawler.value.lock' for update;")
            session.query(sql)
