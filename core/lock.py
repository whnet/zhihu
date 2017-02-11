#!/usr/bin/env python
# coding: utf-8

from __future__ import with_statement

from abc import ABCMeta, abstractmethod


class Lock(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def lock(self):
        raise NotImplementedError

    @abstractmethod
    def unlock(self):
        raise NotImplementedError
