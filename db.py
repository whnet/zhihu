#!/usr/bin/env python
# coding: utf-8

from contextlib import closing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import MYSQL, DEBUG
from model import BaseModel

__all__ = ['init_database', 'Session']
__author__ = 'gatsby'
__version__ = '0.0.1'

_db_conn_string = (
    'mysql+pymysql://{user}:{pass}@{host}:{port}/{db}?charset=utf8')

_engine = create_engine(
    _db_conn_string.format(**MYSQL),
    pool_recycle=3600,
    pool_size=12,
    echo_pool=DEBUG)

Session = sessionmaker(bind=_engine)


def init_database():
    with closing(_engine.connect()) as conn:
        tables = [
            table.name for table in
            BaseModel.metadata.sorted_tables
        ]
        tran = conn.begin()
        try:
            for _table in tables:
                sql = 'drop table if exists `%s`;' % _table
                conn.execute(sql)
            BaseModel.metadata.create_all(_engine)
            tran.commit()
        except:
            tran.rollback()
            raise

if __name__ == '__main__':
    init_database()
