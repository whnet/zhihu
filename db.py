#!/usr/bin/env python
# coding: utf-8

from contextlib import closing
from sqlalchemy import create_engine
from config import MYSQL, DEBUG

__all__ = ['init_database']

_db_conn_string = (
    'mysql+pymysql://{user}:{pass}@{host}:{port}/{db}?charset=utf8')

_engine = create_engine(
    _db_conn_string.format(**MYSQL),
    pool_recycle=3600,
    pool_size=12,
    echo_pool=DEBUG)


def init_database():
    with closing(_engine.connect()) as conn:
        tran = conn.begin()
        try:
            drop_tables = [
                'zhihu_topic', 'zhihu_question',
                'zhihu_anwser', 'zhihu_comment']
            for _table in drop_tables:
                sql = 'drop table if exists `%s`;' % _table
                tran.execute(sql)
            tran.commit()
        except:
            tran.rollback()
            raise

if __name__ == '__main__':
    pass
