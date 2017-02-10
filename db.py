#!/usr/bin/env python
# coding: utf-8

import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import BaseModel
from config import MYSQL, DEBUG

__all__ = ['init_database']

_db_conn_string = (
    'mysql+pymysql://{user}:{pass}@{host}:{port}/{db}?charset=utf8')

_engine = create_engine(
    _db_conn_string.format(**MYSQL),
    pool_size=MYSQL['pool_size'],
    pool_recycle=3600,
    echo_pool=DEBUG)

Session = sessionmaker(bind=_engine)


def init_database():
    with contextlib.closing(_engine.connect()) as connect:
        tables = [table.name for table in BaseModel.metadata.sorted_tables]
        tran = connect.begin()
        try:
            connect.execute(
                "alter database %s character set utf8;" % MYSQL['db'])
            for _table in tables:
                sql = "drop table if exists `%s`;" % _table
                connect.execute(sql)
            BaseModel.metadata.create_all(_engine)
            with open('./init.sql', 'rt') as f:
                sql = f.read()
                connect.execute(sql)
            tran.commit()
        except:
            tran.rollback()
            raise

if __name__ == '__main__':
    init_database()
