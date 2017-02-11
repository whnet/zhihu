#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from sqlalchemy import (  # noqa
    Column, BigInteger, Integer, String,
    DateTime, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Index

BaseModel = declarative_base()


class Proxy(BaseModel):
    __tablename__ = 'proxy'
    __table_args__ = (
        Index('schema_type_index', 'schema_type'),
    )

    id = Column(Integer, primary_key=True)
    schema_type = Column(Integer, nullable=False)
    host = Column(String(32), nullable=False)
    port = Column(Integer, nullable=False)
    user = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    deleted = Column(Integer, default=0, nullable=False)


class AppConfig(BaseModel):
    __tablename__ = 'app_config'
    __table_args__ = (
        Index('config_name_index', 'name'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    value = Column(String(1024), nullable=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(DateTime, default=datetime.now, nullable=False)
