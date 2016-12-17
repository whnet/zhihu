#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from sqlalchemy import (
    Column, BigInteger, Integer, String,
    DateTime, Text)
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
    url = Column(String(255), default='', nullable=False)
    title = Column(String(128), default='', nullable=False)
    summary = Column(String(512), default='', nullable=False)
    like_count = Column(String(12), default='', nullable=False)
    create_time = Column(
        DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, nullable=False)
    deleted = Column(Integer, default=0, nullable=False)


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


class SpiderValue(BaseModel):
    __tablename__ = 'spider_value'
    __table_args__ = (
        Index('spider_value_index', 'name'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    value = Column(String(255), nullable=False)


class Answer(BaseModel):
    __tablename__ = 'zhihu_answer'
    __table_args__ = (
        Index('zhihu_answer_index', 'zhihu_id'),
        Index('zhihu_question_index', 'question_id'),
    )

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    like_count = Column(String(16), nullable=False)
    nick_name = Column(
        String(64), default='', nullable=False)
    create_time = Column(
        DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, nullable=False)
    deleted = Column(Integer, default=0, nullable=False)


class AnswerContent(BaseModel):
    __tablename__ = 'answer_content'

    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, nullable=False)
    content = Column(Text, default='', nullable=False)
