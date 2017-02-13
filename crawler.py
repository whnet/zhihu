#!/usr/bin/env python
# coding: utf-8

from abc import ABCMeta, abstractmethod

from dbs.handler import query_proxies


class Crawler(object):

    __metaclass__ = ABCMeta

    def __init__(self, user=None, password=None):
        self.user = user
        self.proxies = None
        self.password = password
        super(Crawler, self).__init__()

    def load_proxies(self):
        proxies = query_proxies()
        self.proxies = proxies.sort(lambda o: o['score'], reverse=True)

    @abstractmethod
    def login(self):
        raise NotImplementedError

if __name__ == '__main__':
    crawler = Crawler()
