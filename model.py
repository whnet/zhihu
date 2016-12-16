#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from sqlalchemy import (
    Column, BigInteger, Integer, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Index

BaseModel = declarative_base()


class Question(BaseModel):
    __tablename__ = 'zhihu_question'
    __table_args__ = (
        Index('zhihu_question_id', 'zhihu_id'),
    )

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(BigInteger, nullable=False)
    title = Column(String(512), nullable=False)
    summary = Column(String(1024), nullable=False)
    create_time = Column(
        DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, nullable=False)


class Proxy(BaseModel):
    __tablename__ = 'proxy'
    __table_args__ = (
        Index('proxy_score_index', 'score'),
        Index('proxy_schema_index', 'schema_type'),
    )

    id = Column(Integer, primary_key=True)
    host = Column(String(24), default='', nullable=False)
    port = Column(Integer, default=80, nullable=False)
    user = Column(String(32), default='', nullable=False)
    password = Column(String(32), default='', nullable=False)
    schema_type = Column(Integer, default=0, nullable=False)
    score = Column(Integer, default=0, nullable=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(DateTime, default=datetime.now, nullable=False)
    deleted = Column(Integer, default=0, nullable=False)
