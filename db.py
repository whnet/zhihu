#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import

import glob
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbs.model import BaseModel
from config import MYSQL, DEBUG

__all__ = ['init_database', 'Session']

_db_conn_string = (
    'mysql+pymysql://{user}:{pass}@{host}:{port}/{db}?charset=utf8'
)

_engine = create_engine(
    _db_conn_string.format(**MYSQL),
    pool_size=MYSQL['pool_size'],
    pool_recycle=3600,
    echo_pool=DEBUG)

Session = sessionmaker(bind=_engine)


def init_database():
    with contextlib.closing(_engine.connect()) as connect:
        tran = connect.begin()
        try:
            connect.execute(
                "alter database %s character set utf8;" % MYSQL['db'])
            BaseModel.metadata.create_all(_engine)
            for sql_script_file in glob.glob('./sqls/*.sql'):
                with open(sql_script_file, 'rt') as f:
                    for sql in f:
                        connect.execute(sql)
                    tran.commit()
        except:
            tran.rollback()

if __name__ == '__main__':
    init_database()
