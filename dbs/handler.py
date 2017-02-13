#!/usr/bin/env python
# coding: utf-8

import contextlib
from db import Session
from dbs import model_to_dict
from dbs.model import AppConfig, Proxy


def query_app_config(name):
    with contextlib.closing(Session()) as session:
        app_config = session.query(AppConfig).filter(
            AppConfig.name == name).first()
        if app_config is not None:
            return app_config.value


def query_proxies():
    with contextlib.closing(Session()) as session:
        proxies = []
        for _proxy in session.query(Proxy).filter(
                Proxy.deleted == 0).all():
            proxies.append(model_to_dict(_proxy))
        return proxies
