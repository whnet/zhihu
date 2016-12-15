#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from sqlalchemy import (
    Column, BigInteger, Integer, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Index

BaseModel = declarative_base()


class Topic(BaseModel):
    __tablename__ = 'zhihu_topic'
    __table_args__ = (
        Index('zhihu_topic_id', 'zhihu_id'),
    )

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(BigInteger, nullable=False)
    topic = Column(String(64), nullable=False)
    create_time = Column(
        DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, nullable=False)


class Question(BaseModel):
    __tablename__ = 'zhihu_question'
    __table_args__ = (
        Index('zhihu_question_id', 'zhihu_id'),
    )

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(BigInteger, nullable=False)
    question = Column(String(4096), nullable=False)
