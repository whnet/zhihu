#!/usr/bin/env python
# coding: utf-8

import contextlib
from db import Session
from dbs.model import AppConfig


def query_app_config(name):
    with contextlib.closing(Session()) as session:
        app_config = session.query(AppConfig).filter(
            AppConfig.name == name).first()
        if app_config is not None:
            return app_config.value
