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
